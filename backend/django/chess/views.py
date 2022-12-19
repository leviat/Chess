from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, mixins, generics

from chess.models import ChessMatchModel, ChessPieceModel
from chess.serializers import ChessMatchSerializer

default_board_pieces = (
    [
        {"pos": pos, "type": ChessPieceModel.PAWN, "color": ChessPieceModel.BLACK}
        for pos in range(8, 16)
    ]
    + [
        {"pos": pos, "type": ChessPieceModel.PAWN, "color": ChessPieceModel.WHITE}
        for pos in range(48, 56)
    ]
    + [
        {"pos": pos, "type": ChessPieceModel.ROOK, "color": ChessPieceModel.BLACK}
        for pos in (0, 7)
    ]
    + [
        {"pos": pos, "type": ChessPieceModel.ROOK, "color": ChessPieceModel.WHITE}
        for pos in (56, 63)
    ]
    + [
        {
            "pos": pos,
            "type": ChessPieceModel.KNIGHT,
            "color": ChessPieceModel.BLACK,
        }
        for pos in (1, 6)
    ]
    + [
        {
            "pos": pos,
            "type": ChessPieceModel.KNIGHT,
            "color": ChessPieceModel.WHITE,
        }
        for pos in (57, 62)
    ]
    + [
        {
            "pos": pos,
            "type": ChessPieceModel.BISHOP,
            "color": ChessPieceModel.BLACK,
        }
        for pos in (2, 5)
    ]
    + [
        {
            "pos": pos,
            "type": ChessPieceModel.BISHOP,
            "color": ChessPieceModel.WHITE,
        }
        for pos in (58, 61)
    ]
    + [{"pos": 3, "type": ChessPieceModel.QUEEN, "color": ChessPieceModel.BLACK}]
    + [{"pos": 59, "type": ChessPieceModel.QUEEN, "color": ChessPieceModel.WHITE}]
    + [{"pos": 4, "type": ChessPieceModel.KING, "color": ChessPieceModel.BLACK}]
    + [{"pos": 60, "type": ChessPieceModel.KING, "color": ChessPieceModel.WHITE}]
)


class ChessMatchDetail(APIView):
    def get(self, request, format=None):
        if request.query_params.get("id") is None:
            return Response("Specify a room id.", status=status.HTTP_400_BAD_REQUEST)

        try:
            id = request.query_params.get("id")
            chess_match = ChessMatchModel.objects.get(pk=id)
            serializer = ChessMatchSerializer(chess_match)
            return Response(serializer.data)
        except ChessMatchModel.DoesNotExist:
            data = {"id": id, "pieces": default_board_pieces}
            serializer = ChessMatchSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            print(serializer.errors)
            return Response("Specify a room id.", status=status.HTTP_400_BAD_REQUEST)


class ChessMatchTest(APIView):
    """
    View to retrieve and create a chess match for testing
    """

    def get_object(self):
        try:
            return ChessMatchModel.objects.get(pk=ChessMatchModel.TEST_MATCH_ID)
        except ChessMatchModel.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        test_match = self.get_object()
        serializer = ChessMatchSerializer(test_match)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data["id"] = ChessMatchModel.TEST_MATCH_ID
        ChessMatchModel.objects.filter(
            id=ChessMatchModel.TEST_MATCH_ID
        ).delete()  # ensures that we also delete all related data e.g. chess pieces and users
        serializer = ChessMatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(request.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        test_match = self.get_object()
        test_match.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
