import random
from typing import List, Optional

from playchess.board import Board
from playchess.game import Game
from playchess.move import Move
from playchess.piece import Piece


PIECE_SCORES = {Piece.WHITE_KING: 0, Piece.BLACK_KING: 0,
                Piece.WHITE_QUEEN: 9, Piece.BLACK_QUEEN: -9,
                Piece.WHITE_ROOK: 5, Piece.BLACK_ROOK: -5,
                Piece.WHITE_BISHOP: 3, Piece.BLACK_BISHOP: -3,
                Piece.WHITE_KNIGHT: 3, Piece.BLACK_KNIGHT: -3,
                Piece.WHITE_PAWN: 1, Piece.BLACK_PAWN: -1}
CHECKMATE_ABS_SCORE = 1000
STALEMATE_SCORE = 0


def find_random_move(moves: List[Move]) -> Move:
    """Returns a random move from a given list of moves."""

    return random.choice(moves)


def find_best_material_move(game_: Game, moves: List[Move]) -> Move:
    """Returns a move which gives most material advantage."""

    # Assume zero sum game (More positive = White winning, More negative = Black winning)

    # Start with least possible score for each player
    score_to_beat = -CHECKMATE_ABS_SCORE if game_.turn.is_white() else CHECKMATE_ABS_SCORE
    best_move: Optional[Move] = None
    random.shuffle(moves)

    for move in moves:
        game_.make_move(move)

        score = find_material_score(game_)

        if ((score < score_to_beat) and game_.turn.is_white()) or \
                ((score > score_to_beat) and not game_.turn.is_white()):
            score_to_beat = score
            best_move = move

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
