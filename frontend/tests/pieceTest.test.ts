import { beforeEach, describe, expect, it, assert } from 'vitest'
import { PieceType, PieceColor, Board, Piece } from '../src/scripts/ChessClasses'

let board: Board;
let piece: Piece;

beforeEach(() => {
    board = new Board();
    piece = board.spawn(PieceType.KING, PieceColor.WHITE, 18);
})

describe('Piece', () => {

    it('changes position after moving', () => {
        expect(piece.interact(17)).toBeTruthy();
        expect(piece.pos).toEqual(17);
        expect(board.getPiece(17)).toEqual(piece);
        expect(board.getPiece(18)).toBeNull();
    });

    it('replaces other piece after attacking', () => {
        board.spawn(PieceType.PAWN, PieceColor.BLACK, 17);
        expect(piece.interact(17)).toBeTruthy();
        expect(piece.pos).toEqual(17);
        expect(board.getPiece(17)).toEqual(piece);
    });

})