import { beforeEach, describe, expect, it } from 'vitest'
import { PieceType, PieceColor, Board, Piece } from '../src/scripts/ChessClasses'

let board: Board;
let king: Piece;

beforeEach(() => {
    board = new Board();
})

describe('King', () => {
    let adjacentFields = [20, 21, 22, 28, 30, 36, 37, 38];

    it('can move to any adjacent field', () => {
        king = board.spawn(PieceType.KING, PieceColor.WHITE, 29);
        let movableFields = king.movableFields().sort();
        expect(movableFields).toEqual(adjacentFields);
    });

    it('can attack any adjacent field', () => {
        king = board.spawn(PieceType.KING, PieceColor.WHITE, 29);
        adjacentFields.forEach(pos => board.spawn(PieceType.PAWN, PieceColor.BLACK, pos));
        board.spawn(PieceType.BISHOP, PieceColor.BLACK, 0);
        board.spawn(PieceType.BISHOP, PieceColor.BLACK, 44);

        let attackableFields = king.attackableFields().sort();

        expect(attackableFields).toEqual(adjacentFields);
    });

    it('can perform castling if neither pieces have been moved', () => {
        king = board.spawn(PieceType.KING, PieceColor.BLACK, 4);
        let rook = board.spawn(PieceType.ROOK, PieceColor.BLACK, 0);
        king.interact(0);
        expect(king.pos).toEqual(2);
        expect(rook.pos).toEqual(3);
        expect(board.getPiece(2)).toEqual(king);
        expect(board.getPiece(3)).toEqual(rook);
    })

    it('cannot perform castling after either piece has been moved', () => {
        king = board.spawn(PieceType.KING, PieceColor.BLACK, 4);
        let rook = board.spawn(PieceType.ROOK, PieceColor.BLACK, 0);
        king.interact(3);
        king.interact(4);
        expect(king.pos).toEqual(4);
        expect(rook.pos).toEqual(0);
        expect(board.getPiece(4)).toEqual(king);
        expect(board.getPiece(0)).toEqual(rook);
    })

    it('can only move king if he is checked', () => {
        expect(false).toBeTruthy();
    })
})