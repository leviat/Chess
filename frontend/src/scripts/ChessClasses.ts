import { reactive } from "vue";

export enum PieceType {
    KING = 'KI',
    QUEEN = 'QU',
    ROOK = 'RO',
    BISHOP = 'BI',
    KNIGHT = 'KN',
    PAWN = 'PA',
};

export enum PieceColor {
    WHITE = 'W',
    BLACK = 'B',
}

const N = -8;
const E = 1;
const W = -1;
const S = 8;
const NW = - 9;
const NE = - 7;
const SW = 7;
const SE = 9;

function inRow(pos: number, row: number) { //row numbers adhere to chess rows 1-8
    return pos >= (row - 1) * 8 && pos < row * 8;
}

function atLeftBorder(pos: number) {
    return pos % 8 === 0;
}

function atRightBorder(pos: number) {
    return pos % 8 === 7;
}

function atTopBorder(pos: number) {
    return inRow(pos, 1);
}

function atBottomBorder(pos: number) {
    return inRow(pos, 8);
}

export type BoardOccupancy = (Piece | null)[]

export class Board {
    readonly fields: (Piece | null)[]

    constructor() {
        this.fields = reactive(new Array<Piece | null>(63));
        this.fields.fill(null)
    }

    getFields = () => this.fields;

    getPiece = (pos: number) => this.fields[pos];
    isOccupied = (pos: number) => this.fields[pos] !== null;

    getColor(pos: number): PieceColor {
        if (!this.isOccupied(pos)) {
            throw "Field is empty."
        }

        return this.fields[pos]!.color;
    }

    spawn(type: PieceType, color: PieceColor, pos: number): Piece {
        return this.fields[pos] = PieceFactory.create(type, color, pos, this);
    }

    swap(pos: number, otherPos: number) {
        let x = this.fields[pos];
        this.fields[pos] = this.fields[otherPos];
        this.fields[otherPos] = x;

        if (this.fields[pos] !== null)
            this.fields[pos]!.pos = pos;
        if (this.fields[otherPos] !== null)
            this.fields[otherPos]!.pos = otherPos;
    }

    replace(pos: number, replacedPos: number) {
        this.fields[replacedPos] = this.fields[pos];
        this.fields[pos] = null;

        if (this.fields[replacedPos] !== null) {
            this.fields[replacedPos]!.pos = replacedPos;
        }
    }
}

export abstract class Piece {
    readonly type: PieceType;
    readonly color: PieceColor;
    readonly board: Board;
    hasMoved: boolean;
    pos: number;

    constructor(type: PieceType, color: PieceColor, pos: number, board: Board) {
        this.type = type;
        this.color = color;
        this.pos = pos
        this.board = board;
        this.hasMoved = false;
    }

    abstract interactable(): number[];

    movableFields(): number[] {
        return this.interactable().filter(x => !this.board.isOccupied(x));
    }

    attackableFields(): number[] {
        return this.interactable().filter(x => this.board.isOccupied(x) && this.board.getColor(x) !== this.color);
    }

    interact(pos: number): boolean {
        if (this.movableFields().includes(pos) || this.attackableFields().includes(pos)) {
            this.board.replace(this.pos, pos);
            this.hasMoved = true;
            return true;
        }
        return false;
    }
}

const PieceFactory = {
    create(type: PieceType, color: PieceColor, pos: number, board: Board): Piece {
        if (type === PieceType.BISHOP)
            return new Bishop(color, pos, board);
        else if (type === PieceType.KING)
            return new King(color, pos, board);
        else if (type === PieceType.KNIGHT)
            return new Knight(color, pos, board);
        else if (type === PieceType.PAWN)
            return new Pawn(color, pos, board);
        else if (type === PieceType.QUEEN)
            return new Queen(color, pos, board);
        else if (type === PieceType.ROOK)
            return new Rook(color, pos, board);
        else
            throw `Invalid piece type: ${type}`
    }
}

export { PieceFactory }

export class Bishop extends Piece {
    constructor(color: PieceColor, pos: number, board: Board) {
        super(PieceType.BISHOP, color, pos, board);
    }

    interactable(): number[] {
        let fields = new Array<number>();

        let x = this.pos;

        while (!atLeftBorder(x) && !atTopBorder(x)) { // NW
            x += NW;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        x = this.pos;

        while (!atRightBorder(x) && !atTopBorder(x)) { // NE
            x += NE;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        x = this.pos;

        while (!atBottomBorder(x) && !atLeftBorder(x)) { // SW
            x += SW;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        x = this.pos;

        while (!atBottomBorder(x) && !atRightBorder(x)) { // SE
            x += SE;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        return fields;
    }
}

export class Rook extends Piece {
    constructor(color: PieceColor, pos: number, board: Board) {
        super(PieceType.ROOK, color, pos, board);
    }

    interactable(): number[] {
        let fields = new Array<number>();

        let x = this.pos;

        while (!atBottomBorder(x)) {
            x += S;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        x = this.pos;

        while (!atTopBorder(x)) {
            x += N;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        x = this.pos;

        while (!atLeftBorder(x)) {
            x += W;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        x = this.pos;

        while (!atRightBorder(x)) {
            x += E;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        return fields;
    }

    interact(pos: number): boolean {
        if (this.movableFields().includes(pos)) {
            this.board.swap(this.pos, pos);
            return true;
        }
        return false;
    }
}

export class Pawn extends Piece {
    constructor(color: PieceColor, pos: number, board: Board) {
        super(PieceType.PAWN, color, pos, board);
    }

    interactable(): number[] {
        return this.movableFields().concat(this.attackableFields());
    }

    movableFields(): number[] {
        let fields = new Array<number>();

        if (this.color === PieceColor.WHITE) {
            if (this.pos < 8) {
                return [];
            }

            if (this.pos < 56 && this.pos >= 48) {
                fields.push(this.pos - 16);
            }

            fields.push(this.pos - 8);
        }
        else {
            if (this.pos >= 56) {
                return [];
            }

            if (this.pos < 16 && this.pos >= 8) {
                fields.push(this.pos + 16);
            }

            fields.push(this.pos + 8);
        }

        return fields.filter(x => !this.board.isOccupied(x));
    }

    attackableFields(): number[] {
        let fields = new Array<number>();

        if (this.color === PieceColor.WHITE && !atTopBorder(this.pos)) {
            if (!atLeftBorder(this.pos)) {
                fields.push(this.pos + NW);
            }
            if (!atRightBorder(this.pos)) {
                fields.push(this.pos + NE);
            }
        }

        else if (this.color === PieceColor.BLACK && !atBottomBorder(this.pos)) {
            if (!atLeftBorder(this.pos)) {
                fields.push(this.pos + SW);
            }
            if (!atRightBorder(this.pos)) {
                fields.push(this.pos + SE);
            }
        }

        return fields.filter(x => this.board.isOccupied(x) && this.board.getColor(x) !== this.color);
    }

    interact(pos: number): boolean {
        return super.interact(pos);
    }
}

export class Knight extends Piece {
    constructor(color: PieceColor, pos: number, board: Board) {
        super(PieceType.KNIGHT, color, pos, board);
    }

    interactable(): number[] {
        let fields = new Array<number>();

        if (!atTopBorder(this.pos)) {
            if (this.pos % 8 > 1) {
                fields.push(this.pos + N + 2 * W);
            }
            if (this.pos % 8 < 6) {
                fields.push(this.pos + N + 2 * E);
            }
        }

        if (this.pos > 16) {
            if (!atLeftBorder(this.pos)) {
                fields.push(this.pos + 2 * N + W);
            }
            if (!atRightBorder(this.pos)) {
                fields.push(this.pos + 2 * N + E);
            }
        }

        if (this.pos < 48) {
            if (!atLeftBorder(this.pos)) {
                fields.push(this.pos + 2 * S + W);
            }
            if (!atRightBorder(this.pos)) {
                fields.push(this.pos + 2 * S + E);
            }
        }

        if (!atBottomBorder(this.pos)) {
            if (this.pos % 8 > 1) {
                fields.push(this.pos + S + 2 * W);
            }
            if (this.pos % 8 < 6) {
                fields.push(this.pos + S + 2 * E);
            }
        }

        return fields;
    }
}

export class King extends Piece {
    constructor(color: PieceColor, pos: number, board: Board) {
        super(PieceType.KING, color, pos, board);
    }

    interactable(): number[] {
        let fields = new Array<number>();

        if (!atTopBorder(this.pos)) {
            fields.push(this.pos + N);

            if (!atLeftBorder(this.pos)) {
                fields.push(this.pos + N + W);
            }

            if (!atRightBorder(this.pos)) {
                fields.push(this.pos + N + E);
            }
        }

        if (!atBottomBorder(this.pos)) {
            fields.push(this.pos + S);

            if (!atLeftBorder(this.pos)) {
                fields.push(this.pos + S + W);
            }

            if (!atRightBorder(this.pos)) {
                fields.push(this.pos + S + E);
            }
        }

        if (!atLeftBorder(this.pos)) {
            fields.push(this.pos + W);
        }

        if (!atRightBorder(this.pos)) {
            fields.push(this.pos + E);
        }

        return fields;
    }

    isInCheck(pos: number): boolean {
        return this.board.fields.filter(x => x !== null && x!.color !== this.color)
            .map(x => x!.attackableFields()).some(x => x.includes(pos));
    }

    interact(pos: number): boolean {
        if (super.interact(pos))
            return true;

        let otherPiece = this.board.getPiece(pos);
        // castling
        // Neither the king nor the rook has previously moved.
        // There are no pieces between the king and the rook.
        // The king is not currently in check.
        // The king does not pass through a square that is attacked by an opposing piece.
        // The king does not end up in check. (True of any legal move.)

        if (this.hasMoved || !(otherPiece instanceof Rook) || otherPiece.hasMoved || otherPiece.color !== this.color)
            return false;

        let inc = this.pos < pos ? 1 : -1;

        for (let i = this.pos + inc; i != pos && i != this.pos; i += inc) {
            if (this.board.isOccupied(i))
                return false;
        }

        if (this.isInCheck(this.pos) || this.isInCheck(pos))
            return false;

        for (let i = this.pos; i != this.pos && i != pos; i += inc) {
            if(this.isInCheck(i))
                return false;
        }

        this.board.replace(this.pos, this.pos + 2*inc);
        this.board.replace(pos, this.pos - inc);

        return true;
        
    }
}

export class Queen extends Piece {

    constructor(color: PieceColor, pos: number, board: Board) {
        super(PieceType.QUEEN, color, pos, board);
    }

    interactable(): number[] {
        let fields = new Array<number>();

        let x = this.pos;

        while (!atLeftBorder(x) && !atTopBorder(x)) { // NW
            x += NW;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        x = this.pos;

        while (!atRightBorder(x) && !atTopBorder(x)) { // NE
            x += NE;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        x = this.pos;

        while (!atBottomBorder(x) && !atLeftBorder(x)) { // SW
            x += SW;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        x = this.pos;

        while (!atBottomBorder(x) && !atRightBorder(x)) { // SE
            x += SE;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        x = this.pos;

        while (!atBottomBorder(x)) {
            x += S;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        x = this.pos;

        while (!atTopBorder(x)) {
            x += N;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        x = this.pos;

        while (!atLeftBorder(x)) {
            x += W;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        x = this.pos;

        while (!atRightBorder(x)) {
            x += E;
            fields.push(x);

            if (this.board.isOccupied(x)) {
                break;
            }
        }

        return fields;
    }
}