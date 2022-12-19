from rest_framework import serializers
from chess.models import ChessMatchModel, User, ChessPieceModel


class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessPieceModel
        fields = ["pos", "type", "color"]


class ChessMatchSerializer(serializers.ModelSerializer):
    pieces = PieceSerializer(many=True)

    class Meta:
        model = ChessMatchModel
        fields = ["id", "last_accessed", "white", "black", "pieces"]

    def create(self, validated_data):
        pieces_data = validated_data.pop("pieces")
        # ChessMatch.objects.filter(id=validated_data['id']).delete() # ensures that we also delete all related data e.g. chess pieces and users
        chess_match = ChessMatchModel.objects.create(**validated_data)
        for piece_data in pieces_data:
            ChessPieceModel.objects.create(chess_match=chess_match, **piece_data)
        return chess_match

    def update(self, instance, validated_data):
        instance.last_accessed = validated_data.get(
            "last_accessed", instance.last_accessed
        )
        instance.white = validated_data.get("white", instance.white)
        instance.black = validated_data.get("black", instance.black)


class TestMatchSerializer(serializers.ModelSerializer):
    pieces = PieceSerializer(many=True)

    class Meta:
        model = ChessMatchModel
        fields = ["pieces"]

    def create(self, validated_data):
        pieces_data = validated_data.pop("pieces")
        validated_data["id"] = ChessMatchModel.TEST_MATCH_ID
        test_match = ChessMatchModel.objects.create(**validated_data)
        for piece_data in pieces_data:
            ChessPieceModel.objects.create(chess_match=test_match, **piece_data)
        return test_match


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "session_key", "chess_match", "name"]
