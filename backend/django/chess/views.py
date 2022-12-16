from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, mixins, generics

from chess.models import ChessMatch, ChessPiece
from chess.serializers import ChessMatchSerializer

default_board_pieces = [{'position': pos, 'type': ChessPiece.PAWN, 'color': ChessPiece.BLACK} for pos in range(8, 16)] \
    + [{'position': pos, 'type': ChessPiece.PAWN, 'color': ChessPiece.WHITE} for pos in range(48, 56)] \
    + [{'position': pos, 'type': ChessPiece.ROOK, 'color': ChessPiece.BLACK} for pos in (0, 7)] \
    + [{'position': pos, 'type': ChessPiece.ROOK, 'color': ChessPiece.WHITE} for pos in (56, 63)] \
    + [{'position': pos, 'type': ChessPiece.KNIGHT, 'color': ChessPiece.BLACK} for pos in (1, 6)] \
    + [{'position': pos, 'type': ChessPiece.KNIGHT, 'color': ChessPiece.WHITE} for pos in (57, 62)] \
    + [{'position': pos, 'type': ChessPiece.BISHOP, 'color': ChessPiece.BLACK} for pos in (2, 5)] \
    + [{'position': pos, 'type': ChessPiece.BISHOP, 'color': ChessPiece.WHITE} for pos in (58, 61)] \
    + [{'position': 3, 'type': ChessPiece.QUEEN, 'color': ChessPiece.BLACK}] \
    + [{'position': 59, 'type': ChessPiece.QUEEN, 'color': ChessPiece.WHITE}] \
    + [{'position': 4, 'type': ChessPiece.KING, 'color': ChessPiece.BLACK}] \
    + [{'position': 60, 'type': ChessPiece.KING, 'color': ChessPiece.WHITE}]


class ChessMatchDetail(APIView):
    def get(self, request, format=None):
        if request.query_params.get('id') is None:
            return Response("Specify a room id.", status=status.HTTP_400_BAD_REQUEST)

        try:
            id = request.query_params.get('id')
            chess_match = ChessMatch.objects.get(pk=id)
            serializer = ChessMatchSerializer(chess_match)
            return Response(serializer.data)
        except ChessMatch.DoesNotExist:
            data = {'id': id, 'pieces': default_board_pieces}
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
            return ChessMatch.objects.get(pk=ChessMatch.TEST_MATCH_ID)
        except ChessMatch.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        test_match = self.get_object()
        serializer = ChessMatchSerializer(test_match)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data["id"] = ChessMatch.TEST_MATCH_ID
        ChessMatch.objects.filter(id=ChessMatch.TEST_MATCH_ID).delete() # ensures that we also delete all related data e.g. chess pieces and users
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
