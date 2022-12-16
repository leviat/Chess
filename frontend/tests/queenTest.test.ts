import { describe, expect, it } from 'vitest'
import { PieceType, PieceColor, Board } from '../src/scripts/ChessClasses'

describe('Queen', () => {
    let board = new Board();
    let queen = board.spawn(PieceType.QUEEN, PieceColor.WHITE, 29);

    board.spawn(PieceType.ROOK, PieceColor.BLACK, 13);
    board.spawn(PieceType.ROOK, PieceColor.BLACK, 27);
    board.spawn(PieceType.ROOK, PieceColor.BLACK, 31);
    board.spawn(PieceType.ROOK, PieceColor.BLACK, 45);

    board.spawn(PieceType.BISHOP, PieceColor.BLACK, 11);
    board.spawn(PieceType.BISHOP, PieceColor.BLACK, 13);
    board.spawn(PieceType.BISHOP, PieceColor.BLACK, 43);
    board.spawn(PieceType.BISHOP, PieceColor.BLACK, 47);

    let movableFields = queen.movableFields();
    let attackableFields = queen.attackableFields();

    it('can move vertically', () => {
        expect(movableFields).toContain<number>(21);
        expect(movableFields).toContain<number>(37);
    });

    it('can move horizontally', () => {
        expect(movableFields).toContain<number>(28);
        expect(movableFields).toContain<number>(30);
    });

    it('can move diagonally', () => {
        expect(movableFields).toContain<number>(20);
        expect(movableFields).toContain<number>(22);
        expect(movableFields).toContain<number>(36);
        expect(movableFields).toContain<number>(38);
    });

    it('can attack vertically', () => {
        expect(attackableFields).toContain<number>(13);
        expect(attackableFields).toContain<number>(45);
    });

    it('can attack horizontally', () => {
        expect(attackableFields).toContain<number>(27);
        expect(attackableFields).toContain<number>(31);
    });

    it('can attack diagonally', () => {
        expect(attackableFields).toContain<number>(11);
        expect(attackableFields).toContain<number>(13);
        expect(attackableFields).toContain<number>(43);
        expect(attackableFields).toContain<number>(47);
    });
})