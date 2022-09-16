from playchess.game import Game
from playchess.piece import Piece


PIECE_SCORES = {Piece.WHITE_KING: 0, Piece.BLACK_KING: 0,
                Piece.WHITE_QUEEN: 10, Piece.BLACK_QUEEN: -10,
                Piece.WHITE_ROOK: 5, Piece.BLACK_ROOK: -5,
                Piece.WHITE_BISHOP: 3, Piece.BLACK_BISHOP: -3,
                Piece.WHITE_KNIGHT: 3, Piece.BLACK_KNIGHT: -3,
                Piece.WHITE_PAWN: 1, Piece.BLACK_PAWN: -1}
CHECKMATE_ABS_SCORE = 1000.0
STALEMATE_SCORE = 0.0

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
                     Piece.WHITE_BISHOP: ((4, 3, 2, 1, 1, 2, 3, 4),
                                          (3, 4, 3, 2, 2, 3, 4, 4),
                                          (2, 3, 4, 3, 3, 4, 3, 2),
                                          (1, 2, 3, 4, 4, 3, 2, 1),
                                          (1, 2, 3, 4, 4, 3, 2, 1),
                                          (2, 3, 4, 3, 3, 4, 3, 2),
                                          (3, 4, 3, 2, 2, 3, 4, 3),
                                          (4, 3, 2, 1, 1, 2, 3, 4)),
                     Piece.BLACK_BISHOP: ((-4, 3, 2, 1, 1, 2, 3, 4),
                                          (-3, -4, -3, -2, -2, -3, -4, -4),
                                          (-2, -3, -4, -3, -3, -4, -3, -2),
                                          (-1, -2, -3, -4, -4, -3, -2, -1),
                                          (-1, -2, -3, -4, -4, -3, -2, -1),
                                          (-2, -3, -4, -3, -3, -4, -3, -2),
                                          (-3, -4, -3, -2, -2, -3, -4, -3),
                                          (-4, -3, -2, -1, -1, -2, -3, -4)),
                     Piece.WHITE_QUEEN: ((1, 1, 1, 3, 1, 1, 1, 1),
                                         (1, 2, 3, 3, 3, 1, 1, 1),
                                         (1, 4, 3, 3, 3, 4, 2, 1),
                                         (1, 2, 3, 3, 3, 2, 2, 1),
                                         (1, 2, 3, 3, 3, 2, 2, 1),
                                         (1, 4, 3, 3, 3, 4, 2, 1),
                                         (1, 1, 2, 3, 3, 1, 1, 1),
                                         (1, 1, 1, 3, 1, 1, 1, 1)),
                     Piece.BLACK_QUEEN: ((-1, -1, -1, -3, -1, -1, -1, -1),
                                         (-1, -2, -3, -3, -3, -1, -1, -1),
                                         (-1, -4, -3, -3, -3, -4, -2, -1),
                                         (-1, -2, -3, -3, -3, -2, -2, -1),
                                         (-1, -2, -3, -3, -3, -2, -2, -1),
                                         (-1, -4, -3, -3, -3, -4, -2, -1),
                                         (-1, -1, -2, -3, -3, -1, -1, -1),
                                         (-1, -1, -1, -3, -1, -1, -1, -1)),
                     Piece.WHITE_ROOK: ((4, 3, 4, 4, 4, 4, 3, 4),
                                        (4, 4, 4, 4, 4, 4, 4, 4),
                                        (1, 1, 2, 3, 3, 2, 1, 1),
                                        (1, 2, 3, 4, 4, 3, 2, 1),
                                        (1, 2, 3, 4, 4, 3, 2, 1),
                                        (1, 1, 2, 3, 3, 2, 1, 1),
                                        (4, 4, 4, 4, 4, 4, 4, 4),
                                        (4, 3, 4, 4, 4, 4, 3, 4)),
                     Piece.BLACK_ROOK: ((-4, -3, -4, -4, -4, -4, -3, -4),
                                        (-4, -4, -4, -4, -4, -4, -4, -4),
                                        (-1, -1, -2, -3, -3, -2, -1, -1),
                                        (-1, -2, -3, -4, -4, -3, -2, -1),
                                        (-1, -2, -3, -4, -4, -3, -2, -1),
                                        (-1, -1, -2, -3, -3, -2, -1, -1),
                                        (-4, -4, -4, -4, -4, -4, -4, -4),
                                        (-4, -3, -4, -4, -4, -4, -3, -4)),
                     Piece.WHITE_PAWN: ((8, 8, 8, 8, 8, 8, 8, 8),
                                        (8, 8, 8, 8, 8, 8, 8, 8),
                                        (5, 6, 6, 7, 7, 6, 6, 5),
                                        (2, 3, 3, 5, 5, 3, 3, 2),
                                        (1, 2, 3, 4, 4, 3, 2, 1),
                                        (1, 1, 2, 3, 3, 2, 1, 1),
                                        (1, 1, 1, 0, 0, 1, 1, 1),
                                        (0, 0, 0, 0, 0, 0, 0, 0)),
                     Piece.BLACK_PAWN: ((0, 0, 0, 0, 0, 0, 0, 0),
                                        (-1, -1, -1, 0, 0, -1, -1, -1),
                                        (-1, -1, -2, -3, -3, -2, -1, -1),
                                        (-1, -2, -3, -4, -4, -3, -2, -1),
                                        (-2, -3, -3, -5, -5, -3, -3, -2),
                                        (-5, -6, -6, -7, -7, -6, -6, -5),
                                        (-8, -8, -8, -8, -8, -8, -8, -8),
                                        (-8, -8, -8, -8, -8, -8, -8, -8))
                     }


def find_game_score(game: Game, use_positional_scoring: bool) -> float:
    """Finds the score of a chess game based on the material."""

    if game.turn.is_white() and game.check_mate:
        return -CHECKMATE_ABS_SCORE
    elif not game.turn.is_white() and game.check_mate:
        return CHECKMATE_ABS_SCORE
    elif game.stale_mate:
        return STALEMATE_SCORE

    score = 0.0
    for row_num, row in enumerate(game.chess_board):
        for col_num, piece_ in enumerate(row):
            if piece_.is_none():
                continue
            positional_score_matrix = POSITIONAL_SCORES.get(piece_, None)
            positional_score = 0.0
            if positional_score_matrix and use_positional_scoring:
                positional_score = positional_score_matrix[row_num][col_num]

            score = score + float(PIECE_SCORES[piece_]) + (positional_score * 0.1)

    return score
