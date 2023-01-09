import { PieceColor, PieceType, PlayerRole } from "./ChessClasses"
import axios from 'axios';

interface PieceBackend {
    pos: number,
    type: PieceType,
    color: PieceColor,
}

interface ChessRoomBackend {
    id: number,
    last_accessed: Date,
    white: PieceColor | null,
    black: PieceColor | null,
    pieces: Array<PieceBackend>,
    turn: PieceColor,
}

export const api_chess_room = {
    get(room_id: number): Promise<ChessRoomBackend> {
        return axios.get<ChessRoomBackend>(`/api/chess/rooms/${room_id}`).then(
            res => res.data
        ).catch(err => {
            throw err;
        })
    }
}

interface ChessPlayerRoleBackend {
    role: PlayerRole | PieceColor
}

export const api_role = {
    get(room_id: number): Promise<PlayerRole | PieceColor> {
        return axios.get<ChessPlayerRoleBackend>(`/api/chess/role?room_id=${room_id}`).then(
            res => res.data.role
        ).catch(err => {
            throw err
        });
    },

    register(room_id: number, color: PieceColor) {
        return axios.post(`/api/chess/role?room_id=${room_id}&color=${color}`).catch(err => {
            throw err
        })
    }
}