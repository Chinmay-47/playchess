import random
from typing import List, Optional

from playchess.game import Game
from playchess.move import Move
from playchess.piece import Piece


PIECE_SCORES = {Piece.WHITE_KING: 0, Piece.BLACK_KING: 0,
                Piece.WHITE_QUEEN: 950, Piece.BLACK_QUEEN: -950,
                Piece.WHITE_ROOK: 500, Piece.BLACK_ROOK: -500,
                Piece.WHITE_BISHOP: 330, Piece.BLACK_BISHOP: -330,
                Piece.WHITE_KNIGHT: 320, Piece.BLACK_KNIGHT: -320,
                Piece.WHITE_PAWN: 100, Piece.BLACK_PAWN: -100}
CHECKMATE_ABS_SCORE = 10_000
STALEMATE_SCORE = 0


def find_random_move(moves: List[Move]) -> Move:
    """Returns a random move from a given list of moves."""

    return random.choice(moves)


def find_best_move_min_max(game: Game, valid_moves: List[Move], depth: int) -> Move:

    best_move: Optional[Move] = None

    def set_best_move_min_max_recursive(game_: Game, valid_moves_: List[Move], depth_: int, white_to_play: bool):

        nonlocal best_move
        nonlocal depth

        if depth_ == 0:
            return find_material_score(game_)

        random.shuffle(valid_moves_)    # Same moves are repeated if not shuffled

        # Maximizer
        if white_to_play:
            max_score = -CHECKMATE_ABS_SCORE
            for valid_move in valid_moves_:

                game_.make_move(valid_move)
                next_valid_moves = game_.get_valid_moves()
                score = set_best_move_min_max_recursive(game_, next_valid_moves, depth_ - 1, False)

                if score > max_score:
                    max_score = score
                    if depth_ == depth:
                        best_move = valid_move

                game_.undo_move()

            return max_score

        # Minimizer
        else:
            min_score = CHECKMATE_ABS_SCORE

            for valid_move in valid_moves_:

                game_.make_move(valid_move)
                next_valid_moves = game_.get_valid_moves()
                score = set_best_move_min_max_recursive(game_, next_valid_moves, depth_-1, True)

                if score < min_score:
                    min_score = score
                    if depth_ == depth:
                        best_move = valid_move

                game_.undo_move()

            return min_score

    set_best_move_min_max_recursive(game, valid_moves, depth, game.turn.is_white())

    return best_move


def find_best_move_min_max_pruned(game: Game, valid_moves: List[Move], depth: int) -> Move:

    best_move: Optional[Move] = None

    def set_best_move_min_max_recursive(game_: Game, valid_moves_: List[Move], depth_: int, white_to_play: bool,
                                        alpha: int = -CHECKMATE_ABS_SCORE, beta: int = CHECKMATE_ABS_SCORE):

        nonlocal best_move
        nonlocal depth

        if depth_ == 0:
            return find_material_score(game_)

        random.shuffle(valid_moves_)        # Same moves are repeated if not shuffled

        # Maximizer
        if white_to_play:
            max_score = -CHECKMATE_ABS_SCORE
            for valid_move in valid_moves_:

                game_.make_move(valid_move)
                score = set_best_move_min_max_recursive(game_, game_.get_valid_moves(), depth_ - 1, False,
                                                        alpha, beta)

                if score > max_score:
                    max_score = score
                    if depth_ == depth:
                        best_move = valid_move

                game_.undo_move()

                if max_score >= beta:
                    break

                alpha = max(alpha, max_score)

            return max_score

        # Minimizer
        else:
            min_score = CHECKMATE_ABS_SCORE

            for valid_move in valid_moves_:

                game_.make_move(valid_move)
                score = set_best_move_min_max_recursive(game_, game_.get_valid_moves(), depth_-1, True,
                                                        alpha, beta)

                if score < min_score:
                    min_score = score
                    if depth_ == depth:
                        best_move = valid_move

                game_.undo_move()

                if min_score <= alpha:
                    break

                beta = min(beta, min_score)

            return min_score

    set_best_move_min_max_recursive(game, valid_moves, depth, game.turn.is_white())

    return best_move


def find_best_material_move(game_: Game, valid_moves: List[Move]) -> Move:
    """Returns a move which gives most material advantage."""

    score_to_beat = -CHECKMATE_ABS_SCORE if game_.turn.is_white() else CHECKMATE_ABS_SCORE
    best_move: Optional[Move] = None
    random.shuffle(valid_moves)

    for valid_move in valid_moves:
        game_.make_move(valid_move)

        score = find_material_score(game_)

        if ((score < score_to_beat) and game_.turn.is_white()) or \
                ((score > score_to_beat) and not game_.turn.is_white()):
            score_to_beat = score
            best_move = valid_move

        game_.undo_move()

    return best_move


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
