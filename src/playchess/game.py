from typing import List, Optional

import pygame
from playchess.board import Board
from playchess.config import SQUARE_SIZE, DIMENSIONS, LIGHT_SQUARE_COLOUR, DARK_SQUARE_COLOUR
from playchess.images import CHESS_PIECE_IMAGES
from playchess.move import Move


class Game:
    """
    Class to represent a chess game.
    """

    def __init__(self, chess_board: Board):
        self.chess_board = chess_board
        self.move_log: List[Move] = []
        self.captured_pieces: List[str] = []
        self.white_to_move: bool = True

    def _draw_board_pieces(self, screen: pygame.surface.Surface):
        """Draws the chess pieces according to the board state."""

        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):

                # Ignore empty squares
                if self.chess_board.is_empty_square(row, col):
                    continue

                piece = self.chess_board[row][col]
                screen.blit(CHESS_PIECE_IMAGES[piece], pygame.Rect(col * SQUARE_SIZE,
                                                                   row * SQUARE_SIZE,
                                                                   SQUARE_SIZE, SQUARE_SIZE))

    @staticmethod
    def _draw_board(screen: pygame.surface.Surface):
        """Draws the board on a pygame screen."""

        square_colours = [pygame.Color(LIGHT_SQUARE_COLOUR), pygame.Color(DARK_SQUARE_COLOUR)]

        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):

                # Light squares occur when row + column is an even number
                colour_to_draw = square_colours[((row + col) % 2)]
                pygame.draw.rect(screen, colour_to_draw, pygame.Rect(col * SQUARE_SIZE,
                                                                     row * SQUARE_SIZE,
                                                                     SQUARE_SIZE, SQUARE_SIZE))

    def draw(self, screen: pygame.surface.Surface):
        """Draws the current state of the chess game on a pygame screen."""

        self._draw_board(screen)
        self._draw_board_pieces(screen)

    def moves_made(self, last_n: Optional[int] = None) -> List[Move]:
        """Shows moves made previously"""

        if last_n is not None:
            return self.move_log[-last_n:]

        return self.move_log

    @property
    def game_sequence(self) -> str:
        """Shows the sequence of the game played."""
        return " -> ".join([move.name for move in self.move_log])

    @property
    def num_moves_made(self) -> int:
        """Shows number of moves made."""

        return len(self.move_log)

    def make_move(self, move: Move):

        self.chess_board.clear_square(move.from_row, move.from_col)
        if move.piece_is_captured:
            self.captured_pieces.append(move.piece_captured)
        self.chess_board.update_square(move.to_row, move.to_col, move.piece_moved)
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move


def main():
    g = Game(Board())
    print(g.game_sequence)


if __name__ == '__main__':
    main()
