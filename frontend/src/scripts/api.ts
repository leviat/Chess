import { PieceFactory, BoardOccupancy, Piece, PieceColor, PieceType } from "./ChessClasses"
import axios from 'axios';
import { AxiosResponse } from 'axios'

const BASE_URL = 'http://127.0.0.1:8000';

interface PieceBackend {
    pos: number,
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
    get(room_id: number): Promise<Array<PieceBackend>> {
        return axios.get<ChessRoomBackend>(`/api/chess/room?id=${room_id}`).then(
            res => res.data.pieces
        ).catch(err => {
            throw err;
        })
    }
}