from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ChessMatchModel(models.Model):
    TEST_MATCH_ID = 9999999999

    id = models.IntegerField(primary_key=True)
    last_accessed = models.DateTimeField(auto_now_add=True)
    white = models.CharField(null=True, max_length=40)
    black = models.CharField(null=True, max_length=40)

    class Meta:
        ordering = ["last_accessed"]


class ChessPieceModel(models.Model):
    KING = "KI"
    QUEEN = "QU"
    ROOK = "RO"
    BISHOP = "BI"
    KNIGHT = "KN"
    PAWN = "PA"

    TYPE_CHOICES = [
        (KING, "King"),
        (QUEEN, "Queen"),
        (ROOK, "Rook"),
        (BISHOP, "Bishop"),
        (KNIGHT, "Knight"),
        (PAWN, "Pawn"),
    ]

    BLACK = "B"
    WHITE = "W"

    COLOR_CHOICES = [
        (BLACK, "B"),
        (WHITE, "W"),
    ]

    chess_match = models.ForeignKey(
        ChessMatchModel, related_name="pieces", on_delete=models.CASCADE
    )
    pos = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(63)], null=False
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, null=False)
    color = models.CharField(max_length=1, choices=COLOR_CHOICES, null=False)


class User(models.Model):
    session_key = models.CharField(max_length=40)
    chess_match = models.ForeignKey(
        ChessMatchModel, related_name="users", on_delete=models.CASCADE
    )
    name = models.CharField(null=False, max_length=255)

    class Meta:
        unique_together = (
            "session_key",
            "chess_match",
        )
