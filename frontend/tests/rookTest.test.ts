import { describe, expect, it } from 'vitest'
import { PieceType, PieceColor, Board } from '../src/scripts/ChessClasses'

describe('Rook', () => {
    let board = new Board();
    let rook = board.spawn(PieceType.ROOK, PieceColor.WHITE, 29);
    board.spawn(PieceType.ROOK, PieceColor.BLACK, 13);
    board.spawn(PieceType.ROOK, PieceColor.BLACK, 27);
    board.spawn(PieceType.ROOK, PieceColor.BLACK, 31);
    board.spawn(PieceType.ROOK, PieceColor.BLACK, 45);

    let movableFields = rook.movableFields();
    let attackableFields = rook.attackableFields();

    it('can move vertically', () => {
        expect(movableFields).toContain<number>(21);
        expect(movableFields).toContain<number>(37);
    });

    it('can move horizontally', () => {
        expect(movableFields).toContain<number>(28);
        expect(movableFields).toContain<number>(30);
    });

    it('can attack vertically', () => {
        expect(attackableFields).toContain<number>(13);
        expect(attackableFields).toContain<number>(45);
    });

    it('can attack horizontally', () => {
        expect(attackableFields).toContain<number>(27);
        expect(attackableFields).toContain<number>(31);
    });
})