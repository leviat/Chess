import { describe, expect, it } from 'vitest'
import { PieceType, PieceColor, Board } from '../src/scripts/ChessClasses'

describe('Bishop', () => {
    let board = new Board();
    let bishop = board.spawn(PieceType.BISHOP, PieceColor.WHITE, 28);
    board.spawn(PieceType.BISHOP, PieceColor.BLACK, 10);
    board.spawn(PieceType.BISHOP, PieceColor.BLACK, 14);
    board.spawn(PieceType.BISHOP, PieceColor.BLACK, 42);
    board.spawn(PieceType.BISHOP, PieceColor.BLACK, 46);

    let movableFields = bishop.movableFields();
    let attackableFields = bishop.attackableFields();

    it('can move diagonally', () => {
        expect(movableFields).toContain<number>(19);
        expect(movableFields).toContain<number>(21);
        expect(movableFields).toContain<number>(35);
        expect(movableFields).toContain<number>(37);
    });

    it('can attack diagonally', () => {
        expect(attackableFields).toContain<number>(10);
        expect(attackableFields).toContain<number>(14);
        expect(attackableFields).toContain<number>(42);
        expect(attackableFields).toContain<number>(46);
    });

})