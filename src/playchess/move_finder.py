import random
from typing import List, Optional, Union
from abc import ABC

from playchess.game import Game
from playchess.move import Move

from playchess.scorer import CHECKMATE_ABS_SCORE, find_material_score


class MoveFinder(ABC):
    """Class represents a chess move finder."""

    def find_move(self) -> Union[Move, Optional[Move]]:
        """Returns a move that is found."""


class RandomMoveFinder(MoveFinder):
    """Class represents a random move finder in chess."""

    def __init__(self, valid_moves: List[Move]):
        self.valid_moves = valid_moves

    def find_move(self) -> Move:
        """Returns a random move from a given list of moves."""

        return random.choice(self.valid_moves)


class MaterialMoveFinder(MoveFinder):
    """Class represents a purely material based move finder in chess."""

    def __init__(self, game: Game, valid_moves: List[Move]):
        self.game = game
        self.valid_moves = valid_moves

    def find_move(self) -> Optional[Move]:
        """Returns a move which gives most material advantage."""

        score_to_beat = -CHECKMATE_ABS_SCORE if self.game.turn.is_white() else CHECKMATE_ABS_SCORE
        best_move: Optional[Move] = None
        random.shuffle(self.valid_moves)

        for valid_move in self.valid_moves:
            self.game.make_move(valid_move)

            score = find_material_score(self.game)

            if ((score < score_to_beat) and self.game.turn.is_white()) or \
                    ((score > score_to_beat) and not self.game.turn.is_white()):
                score_to_beat = score
                best_move = valid_move

            self.game.undo_move()

        return best_move


class MinMaxMoveFinder(MoveFinder):
    """Class represents a min max based recursive move finder in chess."""

    def __init__(self, game: Game, valid_moves: List[Move], depth):
        self.game = game
        self.valid_moves = valid_moves
        self.depth = depth

    def find_move(self) -> Optional[Move]:
        """Returns a move resulting in best min max score."""

        best_move: Optional[Move] = None

        def set_best_move_min_max_recursive(game_: Game, valid_moves_: List[Move], depth_: int, white_to_play: bool):

            nonlocal best_move

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
                        if depth_ == self.depth:
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
                        if depth_ == self.depth:
                            best_move = valid_move

                    game_.undo_move()

                return min_score

        set_best_move_min_max_recursive(self.game, self.valid_moves, self.depth, self.game.turn.is_white())

        return best_move


class PrunedMinMaxMoveFinder(MoveFinder):
    """Class represents a min max based recursive move finder in chess with alpha beta pruning."""

    def __init__(self, game: Game, valid_moves: List[Move], depth):
        self.game = game
        self.valid_moves = valid_moves
        self.depth = depth

    def find_move(self) -> Optional[Move]:
        """Returns a move resulting in best min max score with alpha beta pruning."""

        best_move: Optional[Move] = None

        def set_best_move_min_max_recursive(game_: Game, valid_moves_: List[Move], depth_: int, white_to_play: bool,
                                            alpha: int = -CHECKMATE_ABS_SCORE, beta: int = CHECKMATE_ABS_SCORE):

            nonlocal best_move

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
                        if depth_ == self.depth:
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
                        if depth_ == self.depth:
                            best_move = valid_move

                    game_.undo_move()

                    if min_score <= alpha:
                        break

                    beta = min(beta, min_score)

                return min_score

        set_best_move_min_max_recursive(self.game, self.valid_moves, self.depth, self.game.turn.is_white())

        return best_move


class PrunedNegaMaxMoveFinder(MoveFinder):
    """Class represents a negamax based recursive move finder in chess with alpha beta pruning."""

    def __init__(self, game: Game, valid_moves: List[Move], depth):
        self.game = game
        self.valid_moves = valid_moves
        self.depth = depth

    def find_move(self) -> Optional[Move]:
        """Returns a move resulting in best min max score with alpha beta pruning."""

        best_move: Optional[Move] = None

        def set_best_move_nega_max_recursive(game_: Game, valid_moves_: List[Move], depth_: int, turn_multiplier: int):

            nonlocal best_move

            if depth_ == 0:
                return turn_multiplier + find_material_score(game_)

            random.shuffle(valid_moves_)        # Same moves are repeated if not shuffled

            # Always maximize for both agents (multiply score by -1 for minimizer)
            score_to_beat = -CHECKMATE_ABS_SCORE
            for valid_move in valid_moves_:

                game_.make_move(valid_move)
                score = -set_best_move_nega_max_recursive(game_, game_.get_valid_moves(), depth_ - 1, -turn_multiplier)

                if score > score_to_beat:
                    score_to_beat = score
                    if depth_ == self.depth:
                        best_move = valid_move

                game_.undo_move()

            return score_to_beat

        _turn_multiplier = 1 if self.game.turn.is_white() else -1
        set_best_move_nega_max_recursive(self.game, self.valid_moves, self.depth, _turn_multiplier)

        return best_move
