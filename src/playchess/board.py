from pprint import pprint
from typing import Optional, List

import pygame
from playchess.config import DIMENSIONS, LIGHT_SQUARE_COLOUR, DARK_SQUARE_COLOUR, SQUARE_SIZE
from playchess.images import CHESS_PIECE_IMAGES


class Board:
    """
    Class to represent a chess board.
    """

    def __init__(self):
        self.board: List[List[str]] = self._get_fresh_board_()
        self.move_log: List[str] = []

    def print(self) -> None:
        pprint(self.board)

    def moves_made(self, last_n: Optional[int] = None) -> List[str]:
        """Shows moves made previously"""

        if last_n is not None:
            return self.move_log[-last_n:]

        return self.move_log

    @property
    def num_moves_made(self):
        """Shows number of moves made."""

        return len(self.move_log)

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

    def _draw_pieces(self, screen: pygame.surface.Surface):
        """Draws the chess pieces according to the board state."""

        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
                piece = self.board[row][col]

                # Ignore empty squares
                if piece != '--':
                    screen.blit(CHESS_PIECE_IMAGES[piece], pygame.Rect(col * SQUARE_SIZE,
                                                                       row * SQUARE_SIZE,
                                                                       SQUARE_SIZE, SQUARE_SIZE))

    @staticmethod
    def _get_fresh_board_() -> List[List[str]]:
        return \
            [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]] + \
            [["bp"] * DIMENSIONS] + \
            [["--"] * DIMENSIONS] * (DIMENSIONS - 4) + \
            [["wp"] * DIMENSIONS] + \
            [["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

    def draw(self, screen: pygame.surface.Surface):
        self._draw_board(screen)
        self._draw_pieces(screen)


def main():
    b = Board()
    b.print()


if __name__ == '__main__':
    main()
