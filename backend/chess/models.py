from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class ChessPieceType(models.TextChoices):
    KING = "KI", _("King")
    QUEEN = "QU", _("Queen")
    ROOK = "RO", _("Rook")
    BISHOP = "BI", _("Bishop")
    KNIGHT = "KN", _("Knight")
    PAWN = "PA", _("Pawn")


class ChessPieceColor(models.TextChoices):
    BLACK = "B", _("Black")
    WHITE = "W", _("White")


class PlayerRole(models.TextChoices):
    OBSERVER = "O", _("Observer")


class ChessMatchModel(models.Model):
    TEST_MATCH_ID = 9999999999

    id = models.IntegerField(primary_key=True)
    last_accessed = models.DateTimeField(auto_now_add=True)
    white = models.CharField(null=True, max_length=40)
    black = models.CharField(null=True, max_length=40)
    turn = models.CharField(
        max_length=1,
        choices=ChessPieceColor.choices,
        default=ChessPieceColor.WHITE,
        null=False,
        blank=False,
    )

    class Meta:
        ordering = ["last_accessed"]


class ChessPieceModel(models.Model):
    chess_match = models.ForeignKey(
        ChessMatchModel, related_name="pieces", on_delete=models.CASCADE
    )
    pos = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(63)], null=False
    )
    type = models.CharField(max_length=2, choices=ChessPieceType.choices, null=False)
    color = models.CharField(max_length=1, choices=ChessPieceColor.choices, null=False)
