from typing import List, Union, Final
from abc import ABC
from .models import ChessMatchModel, ChessPieceModel, ChessPieceType, ChessPieceColor

N: Final = -8
E: Final = 1
W: Final = -1
S: Final = 8
NW: Final = -9
NE: Final = -7
SW: Final = 7
SE: Final = 9


def inRow(pos: int, row: int):  # row numbers adhere to chess rows 1-8
    return pos >= (row - 1) * 8 and pos < row * 8


def atLeftBorder(pos: int):
    return pos % 8 == 0


def atRightBorder(pos: int):
    return pos % 8 == 7


def atTopBorder(pos: int):
    return inRow(pos, 1)


def atBottomBorder(pos: int):
    return inRow(pos, 8)


class Piece:
    pass


class Board:
    def __init__(self, match: ChessMatchModel):
        self.match: ChessMatchModel = match
        self.fields = [None for i in range(64)]
        for piece in match.pieces.all():
            self.fields[piece.pos] = PieceFactory.create(
                piece.type, piece.color, piece.pos, self
            )

    def getPiece(self, pos: int) -> Union[Piece, None]:
        return self.fields[pos]

    def isOccupied(self, pos: int) -> bool:
        return self.fields[pos] != None

    def getColor(self, pos: int):
        if not self.isOccupied(pos):
            raise Exception("Field is empty.")

        return self.fields[pos].color

    def spawn(self, pieceType, color, pos: int) -> Piece:
        self.fields[pos] = PieceFactory.create(self, pieceType, color, pos)
        self.match.pieces.add(
            ChessPieceModel(
                chess_match=self.match, pos=pos, type=pieceType, color=color
            )
        )
        return self.fields[pos]

    def swap(self, pos: int, otherPos: int):

        x = self.fields[pos]
        self.fields[pos] = self.fields[otherPos]
        self.fields[otherPos] = x
        self.fields[pos].pos = pos
        self.fields[otherPos].pos = otherPos

        # remember that the pieces have been swapped in this instance
        # if otherPos is occupied then the there is a piece at pos in the database that we need to update
        if self.isOccupied(otherPos):
            p = self.match.pieces.get(pos=pos)
            p.pos = otherPos
            p.save()

        if self.isOccupied(pos):
            p = self.match.pieces.get(pos=otherPos)
            p.pos = pos
            p.save()

    def replace(self, pos: int, replacedPos: int):

        self.fields[replacedPos] = self.fields[pos]
        self.fields[pos] = None

        if self.isOccupied(replacedPos):
            self.fields[replacedPos].pos = replacedPos

        # if we moved a piece to replacedPos
        try:
            p = self.match.pieces.get(pos=replacedPos)
            p.delete()
        except ChessPieceModel.DoesNotExist:
            pass

        if self.isOccupied(replacedPos):
            p = self.match.pieces.get(pos=pos)
            p.pos = replacedPos
            p.save()


class Piece(ABC):
    def __init__(self, pieceType, color, pos: int, board: Board):
        self.pieceType = pieceType
        self.color = color
        self.pos: int = pos
        self.board: Board = board
        self.hasMoved: bool = False

    def interactable(self) -> List[int]:
        pass

    def movableFields(self) -> List[int]:
        return [
            field for field in self.interactable() if not self.board.isOccupied(field)
        ]

    def attackableFields(self) -> List[int]:
        return [
            field
            for field in self.interactable()
            if self.board.isOccupied(field) and self.board.getColor(field) != self.color
        ]

    def interact(self, pos: int) -> bool:
        if pos in self.movableFields() or pos in self.attackableFields():
            self.board.replace(self.pos, pos)
            self.hasMoved = True
            return True

        return False


class Bishop(Piece):
    def __init__(self, color, pos: int, board: Board):
        super().__init__(ChessPieceType.BISHOP, color, pos, board)

    def interactable(self) -> List[int]:
        fields = list()

        x = self.pos

        while not atLeftBorder(x) and not atTopBorder(x):  # NW
            x += NW
            fields.append(x)

            if self.board.isOccupied(x):
                break

        x = self.pos

        while not atRightBorder(x) and not atTopBorder(x):  # NE
            x += NE
            fields.append(x)

            if self.board.isOccupied(x):
                break

        x = self.pos

        while not atBottomBorder(x) and not atLeftBorder(x):  # SW
            x += SW
            fields.append(x)

            if self.board.isOccupied(x):
                break

        x = self.pos

        while not atBottomBorder(x) and not atRightBorder(x):  # SE
            x += SE
            fields.append(x)

            if self.board.isOccupied(x):
                break

        return fields


class Rook(Piece):
    def __init__(self, color, pos: int, board: Board):
        super().__init__(ChessPieceType.ROOK, color, pos, board)

    def interactable(self) -> List[int]:
        fields = list()

        x = self.pos

        while not atBottomBorder(x):
            x += S
            fields.append(x)

            if self.board.isOccupied(x):
                break

        x = self.pos

        while not atTopBorder(x):
            x += N
            fields.append(x)

            if self.board.isOccupied(x):
                break

        x = self.pos

        while not atLeftBorder(x):
            x += W
            fields.append(x)

            if self.board.isOccupied(x):
                break

        x = self.pos

        while not atRightBorder(x):
            x += E
            fields.append(x)

            if self.board.isOccupied(x):
                break

        return fields

    def interact(self, pos: int) -> bool:
        if self.movableFields().includes(pos):
            self.board.swap(self.pos, pos)
            return True

        return False


class Pawn(Piece):
    def __init__(self, color, pos: int, board: Board):
        super().__init__(ChessPieceType.PAWN, color, pos, board)

    def interactable(self) -> List[int]:
        return self.movableFields().concat(self.attackableFields())

    def movableFields(self) -> List[int]:
        fields = list()

        if self.color == ChessPieceColor.WHITE:
            if self.pos < 8:
                return []

            if self.pos < 56 and self.pos >= 48:
                fields.append(self.pos - 16)

            fields.append(self.pos - 8)

        else:
            if self.pos >= 56:
                return []

            if self.pos < 16 and self.pos >= 8:
                fields.append(self.pos + 16)

            fields.append(self.pos + 8)

        return [field for field in fields if not self.board.isOccupied(field)]

    def attackableFields(self) -> List[int]:
        fields = list()

        if self.color == ChessPieceColor.WHITE and not atTopBorder(self.pos):
            if not atLeftBorder(self.pos):
                fields.append(self.pos + NW)

            if not atRightBorder(self.pos):
                fields.append(self.pos + NE)

        elif self.color == ChessPieceColor.BLACK and not atBottomBorder(self.pos):
            if not atLeftBorder(self.pos):
                fields.append(self.pos + SW)

            if not atRightBorder(self.pos):
                fields.append(self.pos + SE)

        return [
            field
            for field in fields
            if self.board.isOccupied(field) and self.board.getColor(field) != self.color
        ]

    def interact(self, pos: int) -> bool:
        return super().interact(pos)


class Knight(Piece):
    def __init__(self, color, pos: int, board: Board):
        super().__init__(ChessPieceType.KNIGHT, color, pos, board)

    def interactable(self) -> List[int]:
        fields = list()

        if not atTopBorder(self.pos):
            if self.pos % 8 > 1:
                fields.append(self.pos + N + 2 * W)

            if self.pos % 8 < 6:
                fields.append(self.pos + N + 2 * E)

        if self.pos > 16:
            if not atLeftBorder(self.pos):
                fields.append(self.pos + 2 * N + W)

            if not atRightBorder(self.pos):
                fields.append(self.pos + 2 * N + E)

        if self.pos < 48:
            if not atLeftBorder(self.pos):
                fields.append(self.pos + 2 * S + W)

            if not atRightBorder(self.pos):
                fields.append(self.pos + 2 * S + E)

        if not atBottomBorder(self.pos):
            if self.pos % 8 > 1:
                fields.append(self.pos + S + 2 * W)

            if self.pos % 8 < 6:
                fields.append(self.pos + S + 2 * E)

        return fields


class King(Piece):
    def __init__(self, color, pos: int, board: Board):
        super().__init__(ChessPieceType.KING, color, pos, board)

    def interactable(self) -> List[int]:
        fields = list()

        if not atTopBorder(self.pos):
            fields.append(self.pos + N)

            if not atLeftBorder(self.pos):
                fields.append(self.pos + N + W)

            if not atRightBorder(self.pos):
                fields.append(self.pos + N + E)

        if not atBottomBorder(self.pos):
            fields.append(self.pos + S)

            if not atLeftBorder(self.pos):
                fields.append(self.pos + S + W)

            if not atRightBorder(self.pos):
                fields.append(self.pos + S + E)

        if not atLeftBorder(self.pos):
            fields.append(self.pos + W)

        if not atRightBorder(self.pos):
            fields.append(self.pos + E)

        return fields

    def isInCheck(self, pos: int) -> bool:
        enemies: List[Piece] = [
            x
            for x in self.board.fields
            if self.board.isOccupied(x) and self.board.getColor(x) != self.color
        ]
        fieldsInCheck: set = {
            field for enemy in enemies for field in enemy.attackableFields()
        }
        return pos in fieldsInCheck

    def interact(self, pos: int) -> bool:
        if super().interact(pos):
            return True

        otherPiece = self.board.getPiece(pos)
        # castling
        # Neither the king nor the rook has previously moved.
        # There are no pieces between the king and the rook.
        # The king is not currently in check.
        # The king does not pass through a square that is attacked by an opposing piece.
        # The king does not end up in check. (True of any legal move.)

        if (
            self.hasMoved
            or not isinstance(otherPiece, Rook)
            or otherPiece.hasMoved
            or otherPiece.color != self.color
        ):
            return False

        inc = 1 if self.pos < pos else -1
        i = self.pos + inc

        while i != pos and i != self.pos:
            if self.board.isOccupied(i):
                return False
            i += inc

        if self.isInCheck(self.pos) or self.isInCheck(pos):
            return False

        i = self.pos
        while i != self.pos and i != pos:
            if self.isInCheck(i):
                return False
            i += inc

        self.board.replace(self.pos, self.pos + 2 * inc)
        self.board.replace(pos, self.pos - inc)
        return True


class Queen(Piece):
    def __init__(self, color, pos: int, board: Board):
        super().__init__(ChessPieceType.QUEEN, color, pos, board)

    def interactable(self) -> List[int]:
        fields = list()

        x = self.pos

        while not atLeftBorder(x) and not atTopBorder(x):  # NW
            x += NW
            fields.append(x)

            if self.board.isOccupied(x):
                break

        x = self.pos

        while not atRightBorder(x) and not atTopBorder(x):  # NE
            x += NE
            fields.append(x)

            if self.board.isOccupied(x):
                break

        x = self.pos

        while not atBottomBorder(x) and not atLeftBorder(x):  # SW
            x += SW
            fields.append(x)

            if self.board.isOccupied(x):
                break

        x = self.pos

        while not atBottomBorder(x) and not atRightBorder(x):  # SE
            x += SE
            fields.append(x)

            if self.board.isOccupied(x):
                break

        x = self.pos

        while not atBottomBorder(x):
            x += S
            fields.append(x)

            if self.board.isOccupied(x):
                break

        x = self.pos

        while not atTopBorder(x):
            x += N
            fields.append(x)

            if self.board.isOccupied(x):
                break

        x = self.pos

        while not atLeftBorder(x):
            x += W
            fields.append(x)

            if self.board.isOccupied(x):
                break

        x = self.pos

        while not atRightBorder(x):
            x += E
            fields.append(x)

            if self.board.isOccupied(x):
                break

        return fields


class PieceFactory:
    @staticmethod
    def create(pieceType, color, pos: int, board: Board) -> Piece:
        if pieceType == ChessPieceType.BISHOP:
            return Bishop(color, pos, board)
        elif pieceType == ChessPieceType.KING:
            return King(color, pos, board)
        elif pieceType == ChessPieceType.KNIGHT:
            return Knight(color, pos, board)
        elif pieceType == ChessPieceType.PAWN:
            return Pawn(color, pos, board)
        elif pieceType == ChessPieceType.QUEEN:
            return Queen(color, pos, board)
        elif pieceType == ChessPieceType.ROOK:
            return Rook(color, pos, board)
        else:
            raise Exception(f"Invalid piece type: {pieceType}")
