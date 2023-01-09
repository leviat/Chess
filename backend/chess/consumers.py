import json
import logging
from datetime import datetime

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import DenyConnection
from chess.models import ChessMatchModel, ChessPieceColor
from chess.serializers import ChessMatchSerializer
from asgiref.sync import async_to_sync
from .game_logic import Board

from chess.models import ChessMatchModel, ChessPieceType, ChessPieceColor
from chess.serializers import ChessMatchSerializer

default_board_pieces = (
    [
        {"pos": pos, "type": ChessPieceType.PAWN, "color": ChessPieceColor.BLACK}
        for pos in range(8, 16)
    ]
    + [
        {"pos": pos, "type": ChessPieceType.PAWN, "color": ChessPieceColor.WHITE}
        for pos in range(48, 56)
    ]
    + [
        {"pos": pos, "type": ChessPieceType.ROOK, "color": ChessPieceColor.BLACK}
        for pos in (0, 7)
    ]
    + [
        {"pos": pos, "type": ChessPieceType.ROOK, "color": ChessPieceColor.WHITE}
        for pos in (56, 63)
    ]
    + [
        {
            "pos": pos,
            "type": ChessPieceType.KNIGHT,
            "color": ChessPieceColor.BLACK,
        }
        for pos in (1, 6)
    ]
    + [
        {
            "pos": pos,
            "type": ChessPieceType.KNIGHT,
            "color": ChessPieceColor.WHITE,
        }
        for pos in (57, 62)
    ]
    + [
        {
            "pos": pos,
            "type": ChessPieceType.BISHOP,
            "color": ChessPieceColor.BLACK,
        }
        for pos in (2, 5)
    ]
    + [
        {
            "pos": pos,
            "type": ChessPieceType.BISHOP,
            "color": ChessPieceColor.WHITE,
        }
        for pos in (58, 61)
    ]
    + [{"pos": 3, "type": ChessPieceType.QUEEN, "color": ChessPieceColor.BLACK}]
    + [{"pos": 59, "type": ChessPieceType.QUEEN, "color": ChessPieceColor.WHITE}]
    + [{"pos": 4, "type": ChessPieceType.KING, "color": ChessPieceColor.BLACK}]
    + [{"pos": 60, "type": ChessPieceType.KING, "color": ChessPieceColor.WHITE}]
)


class ChessConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.layer_name = f"chess_{self.room_name}"

        try:  # load match
            chess_match = ChessMatchModel.objects.get(id=self.room_name)
            chess_match.last_accessed = datetime.now()
            chess_match.save()
            serializer = ChessMatchSerializer(chess_match)

        except ChessMatchModel.DoesNotExist:  # register match
            data = {"id": self.room_name, "pieces": default_board_pieces}
            serializer = ChessMatchSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                chess_match = serializer.instance
            else:
                logging.error(serializer.errors)
                raise DenyConnection("Room could not be created.")

        self.board = Board(chess_match)
        async_to_sync(self.channel_layer.group_add)(self.layer_name, self.channel_name)
        self.accept()
        self.send(
            json.dumps(
                {
                    "type": "state",
                    "data": {
                        "pieces": serializer.data["pieces"],
                        "turn": serializer.data["turn"],
                    },
                }
            )
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.layer_name, self.channel_name
        )

    def receive_interaction_message(self, msg):
        chess_match = ChessMatchModel.objects.get(id=self.room_name)
        piece = self.board.getPiece(msg["source"])
        player_color = None

        if self.scope["session"].session_key == chess_match.white:
            player_color = ChessPieceColor.WHITE
        elif self.scope["session"].session_key == chess_match.black:
            player_color = ChessPieceColor.BLACK

        if (
            piece is None
            or piece.color != player_color
            or player_color != chess_match.turn
        ):
            return

        if not piece.interact(msg["target"]):
            return

        chess_match.turn = (
            ChessPieceColor.WHITE
            if chess_match.turn == ChessPieceColor.BLACK
            else ChessPieceColor.BLACK
        )
        chess_match.save()

        async_to_sync(self.channel_layer.group_send)(
            self.layer_name,
            {
                "type": "interaction",
                "data": {
                    "color": player_color,
                    "source": msg["source"],
                    "target": msg["target"],
                },
            },
        )

    def receive(self, text_data):
        msg = json.loads(text_data)

        if msg["type"] == "interaction":
            self.receive_interaction_message(msg["data"])

    def interaction(self, msg):
        self.send(json.dumps({"type": msg["type"], "data": msg["data"]}))
