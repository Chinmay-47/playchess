from playchess.game import Game
from playchess.piece import Piece


PIECE_SCORES = {Piece.WHITE_KING: 0, Piece.BLACK_KING: 0,
                Piece.WHITE_QUEEN: 950, Piece.BLACK_QUEEN: -950,
                Piece.WHITE_ROOK: 500, Piece.BLACK_ROOK: -500,
                Piece.WHITE_BISHOP: 330, Piece.BLACK_BISHOP: -330,
                Piece.WHITE_KNIGHT: 320, Piece.BLACK_KNIGHT: -320,
                Piece.WHITE_PAWN: 100, Piece.BLACK_PAWN: -100}
CHECKMATE_ABS_SCORE = 10_000
STALEMATE_SCORE = 0


def find_material_score(game: Game) -> int:
    """Finds the score of a based on the material."""

    if game.turn.is_white() and game.check_mate:
        return -CHECKMATE_ABS_SCORE
    elif not game.turn.is_white() and game.check_mate:
        return CHECKMATE_ABS_SCORE
    elif game.stale_mate:
        return STALEMATE_SCORE

    score = 0
    for row in game.chess_board:
        for piece_ in row:
            if piece_.is_none():
                continue
            score += PIECE_SCORES[piece_]

    return score
