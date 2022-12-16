import { PieceFactory, BoardOccupancy, Piece, PieceColor, PieceType } from "./ChessClasses"
import axios from 'axios';
import {AxiosResponse} from 'axios'

const BASE_URL = 'http://127.0.0.1:8000';

interface PieceBackend {
    position: number,
    type: PieceType,
    color: PieceColor,
}

interface ChessRoomBackend {
  id: number,
  last_accessed: Date,
  white: string | null,
  black: string | null,
  pieces: Array<PieceBackend>
}

export const api_chess_room = {
    get(room_id: number): Promise<BoardOccupancy> {
        return axios.get<ChessRoomBackend>(`/api/chess/room?id=${room_id}`).then(
            res => {
                let chess_board = Array<Piece | null>(63);
                chess_board.fill(null);
                for (const piece of res.data.pieces) {
                    chess_board[piece.position] = PieceFactory.create(piece.type, piece.color, piece.position);
                }
                return chess_board;
            }
        ).catch(err => {
            throw err;
        })
    }
}