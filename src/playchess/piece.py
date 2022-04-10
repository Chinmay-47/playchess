from enum import Enum, unique


@unique
class Piece(Enum):
    """Class to represent a piece in chess."""

    WHITE_ROOK = "wR"
    WHITE_KNIGHT = "wN"
    WHITE_BISHOP = "wB"
    WHITE_QUEEN = "wQ"
    WHITE_KING = "wK"
    WHITE_PAWN = "wp"

    BLACK_ROOK = "bR"
    BLACK_KNIGHT = "bN"
    BLACK_BISHOP = "bB"
    BLACK_QUEEN = "bQ"
    BLACK_KING = "bK"
    BLACK_PAWN = "bp"

    def is_white(self):
        return "WHITE_" in self.name
