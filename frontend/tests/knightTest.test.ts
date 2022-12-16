import exp from 'constants';
import { beforeEach, describe, expect, it } from 'vitest'
import { PieceType, PieceColor, Board, Piece, Knight } from '../src/scripts/ChessClasses'

let board: Board;
let knight: Piece;

beforeEach(() => {
    board = new Board();
    knight = board.spawn(PieceType.KNIGHT, PieceColor.WHITE, 29);
})

describe('Knight', () => {
    let jumpingSpots = [19, 12, 14, 23, 39, 46, 44, 35] // clockwise enumeration starting at 9 o clock
    jumpingSpots.sort();

    it('can jump', () => {
        let movableFields = knight.movableFields().sort();
        expect(movableFields).toEqual(jumpingSpots);
    });

    it('changes position after moving', () => {
        expect(knight.interact(19)).toBeTruthy();
        expect(knight.pos).toEqual(19);
        expect(board.getPiece(19)).toEqual(knight);
    })

    it('can jump attack', () => {
        jumpingSpots.forEach(pos => board.spawn(PieceType.BISHOP, PieceColor.BLACK, pos));

        // these two should not be attackable
        board.spawn(PieceType.ROOK, PieceColor.BLACK, 0);
        board.spawn(PieceType.ROOK, PieceColor.BLACK, 1);

        let attackableFields = knight.attackableFields().sort();

        expect(attackableFields).toEqual(jumpingSpots);
    });
})