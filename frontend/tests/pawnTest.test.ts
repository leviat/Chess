import { describe, assert, expect, it, beforeEach } from 'vitest'
import { PieceType, PieceColor, Board, Piece } from '../src/scripts/ChessClasses'

let board: Board;
let pawn: Piece;

beforeEach(() => {
    board = new Board();
})

describe('White Pawn', () => {
    it('can move one step ahead', () => {
        let pawn = board.spawn(PieceType.PAWN, PieceColor.WHITE, 52);
        expect(pawn.movableFields()).toContain(44);
    });

    it('can move two steps ahead in initial position', () => {
        let pawn = board.spawn(PieceType.PAWN, PieceColor.WHITE, 52);
        expect(pawn.movableFields()).toContain(36);
    });

    it('cannot move two steps ahead outside of initial position', () => {
        let pawn = board.spawn(PieceType.PAWN, PieceColor.WHITE, 16);
        expect(pawn.movableFields()).not.toContain(0);
    });

    it('can attack diagonally', () => {
        let pawn = board.spawn(PieceType.PAWN, PieceColor.WHITE, 52);
        board.spawn(PieceType.PAWN, PieceColor.BLACK, 45);
        expect(pawn.attackableFields()).toEqual([45]);
    });

    it('can attack en passant', () => {
        expect(true).toBeFalsy();
    });
})

describe('Black Pawn', () => {
    it('can move one step ahead', () => {
        let pawn = board.spawn(PieceType.PAWN, PieceColor.BLACK, 9);
        expect(pawn.movableFields()).toContain(17);
    });

    it('can move two steps ahead in initial position', () => {
        let pawn = board.spawn(PieceType.PAWN, PieceColor.BLACK, 9);
        expect(pawn.movableFields()).toContain(25);
    });

    it('cannot move two steps ahead outside of initial position', () => {
        let pawn = board.spawn(PieceType.PAWN, PieceColor.BLACK, 21);
        expect(pawn.movableFields()).not.toContain([37]);
    });

    it('can attack diagonally', () => {
        let pawn = board.spawn(PieceType.PAWN, PieceColor.BLACK, 9);
        board.spawn(PieceType.PAWN, PieceColor.WHITE, 16);
        expect(pawn.attackableFields()).toEqual([16]);
    });

    it('can attack en passant', () => {
        expect(true).toBeFalsy();
    });

    it('can be turned into another piece at the end of the board', () => {
        expect(true).toBeFalsy();
    })
})