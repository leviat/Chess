from rest_framework import serializers
from chess.models import ChessMatchModel, ChessPieceModel


class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessPieceModel
        fields = ["pos", "type", "color"]


class ChessMatchSerializer(serializers.ModelSerializer):
    pieces = PieceSerializer(many=True)

    class Meta:
        model = ChessMatchModel
        fields = [
            "id",
            "last_accessed",
            "pieces",
            "turn",
        ]

    def create(self, validated_data) -> ChessMatchModel:
        pieces_data = validated_data.pop("pieces")
        chess_match = ChessMatchModel.objects.create(**validated_data)
        for piece_data in pieces_data:
            ChessPieceModel.objects.create(chess_match=chess_match, **piece_data)
        return chess_match


class ChessMatchInfoSerializer(serializers.ModelSerializer):
    white_assigned = serializers.SerializerMethodField("is_white_assigned")
    black_assigned = serializers.SerializerMethodField("is_black_assigned")

    class Meta:
        model = ChessMatchModel
        fields = [
            "id",
            "white_assigned",
            "black_assigned",
        ]

    def is_white_assigned(self, obj: ChessMatchModel) -> bool:
        return obj.white is not None

    def is_black_assigned(self, obj: ChessMatchModel) -> bool:
        return obj.black is not None
