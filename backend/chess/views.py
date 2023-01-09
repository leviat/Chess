from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, mixins, generics

from chess.models import ChessMatchModel, ChessPieceType, ChessPieceColor, PlayerRole
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


class ChessMatchDetail(APIView):
    def get(self, request, format=None):
        if request.query_params.get("id") is None:
            return Response("Specify a room id.", status=status.HTTP_400_BAD_REQUEST)

        try:
            id = request.query_params.get("id")
            chess_match = ChessMatchModel.objects.get(pk=id)
            serializer = ChessMatchSerializer(chess_match)

            if chess_match.black is not None:
                serializer.data["black"] = chess_match.users.get(
                    session_key=chess_match.black
                ).name

            if chess_match.white is not None:
                serializer.data["white"] = chess_match.users.get(
                    session_key=chess_match.white
                ).name

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


class ChessMatchRole(APIView):
    def get(self, request, format=None):
        if request.query_params.get("room_id") is None:
            return Response("Specify a room id.", status=status.HTTP_400_BAD_REQUEST)
        try:
            id = request.query_params.get("room_id")
            chess_match = ChessMatchModel.objects.get(pk=id)
        except ChessMatchModel.DoesNotExist:
            return Response("Match does not exist", status=status.HTTP_404_NOT_FOUND)

        if chess_match.white == request.session.session_key:
            return Response(
                data={"role": ChessPieceColor.WHITE}, status=status.HTTP_200_OK
            )

        if chess_match.black == request.session.session_key:
            return Response(
                data={"role": ChessPieceColor.BLACK}, status=status.HTTP_200_OK
            )

        return Response(data={"role": PlayerRole.OBSERVER}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if request.query_params.get("room_id") is None:
            return Response("Specify a room id.", status=status.HTTP_400_BAD_REQUEST)

        if request.session.session_key is None:
            return Response(
                "Cookies have not been set. Cannot identify user.",
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            id = request.query_params.get("room_id")
            chess_match = ChessMatchModel.objects.get(pk=id)
        except ChessMatchModel.DoesNotExist:
            return Response("Match does not exist", status=status.HTTP_404_NOT_FOUND)

        if (
            chess_match.black == request.session.session_key
            or chess_match.white == request.session.session_key
        ):
            return Response(
                "This player has already claimed a player color.",
                status=status.HTTP_403_FORBIDDEN,
            )

        if request.query_params.get("color") == ChessPieceColor.BLACK:
            if chess_match.black is not None:
                return Response(
                    "Player color has already been claimed.",
                    status=status.HTTP_403_FORBIDDEN,
                )
            chess_match.black = request.session.session_key
            chess_match.save()
            return Response(status=status.HTTP_200_OK)
        elif request.query_params.get("color") == ChessPieceColor.WHITE:
            if chess_match.white is not None:
                return Response(
                    "Player color has already been claimed.",
                    status=status.HTTP_403_FORBIDDEN,
                )
            chess_match.white = request.session.session_key
            chess_match.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                "Specify the player's color.", status=status.HTTP_400_BAD_REQUEST
            )
