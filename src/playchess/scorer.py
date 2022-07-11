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

POSITIONAL_SCORES = {Piece.WHITE_KNIGHT: ((1, 1, 1, 1, 1, 1, 1, 1),
                                          (1, 2, 2, 2, 2, 2, 2, 1),
                                          (1, 2, 3, 3, 3, 3, 2, 1),
                                          (1, 2, 3, 4, 4, 3, 2, 1),
                                          (1, 2, 3, 4, 4, 3, 2, 1),
                                          (1, 2, 3, 3, 3, 3, 2, 1),
                                          (1, 2, 2, 2, 2, 2, 2, 1),
                                          (1, 1, 1, 1, 1, 1, 1, 1)),
                     Piece.BLACK_KNIGHT: ((-1, -1, -1, -1, -1, -1, -1, -1),
                                          (-1, -2, -2, -2, -2, -2, -2, -1),
                                          (-1, -2, -3, -3, -3, -3, -2, -1),
                                          (-1, -2, -3, -4, -4, -3, -2, -1),
                                          (-1, -2, -3, -4, -4, -3, -2, -1),
                                          (-1, -2, -3, -3, -3, -3, -2, -1),
                                          (-1, -2, -2, -2, -2, -2, -2, -1),
                                          (-1, -1, -1, -1, -1, -1, -1, -1)),
                     }


def find_game_score(game: Game, use_positional_scoring: bool = True) -> int:
    """Finds the score of a chess game based on the material."""

    if game.turn.is_white() and game.check_mate:
        return -CHECKMATE_ABS_SCORE
    elif not game.turn.is_white() and game.check_mate:
        return CHECKMATE_ABS_SCORE
    elif game.stale_mate:
        return STALEMATE_SCORE

    score = 0
    for row_num, row in enumerate(game.chess_board):
        for col_num, piece_ in enumerate(row):
            if piece_.is_none():
                continue
            positional_score_matrix = POSITIONAL_SCORES.get(piece_, None)
            positional_score = 0
            if positional_score_matrix and use_positional_scoring:
                positional_score = positional_score_matrix[row_num][col_num]

            score = score + PIECE_SCORES[piece_] + (positional_score * 0.1)

    return score
