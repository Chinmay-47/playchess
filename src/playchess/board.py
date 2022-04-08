from pprint import pprint
from typing import Optional, List, Dict, Tuple

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
        self.white_to_move: bool = True

        # Mappings between notation and matrix positions
        self.ranks_to_rows: Dict[str, int] = {str(i + 1): DIMENSIONS - 1 - i for i in range(DIMENSIONS)}
        self.rows_to_ranks: Dict[int, str] = {val: key for key, val in self.ranks_to_rows.items()}
        self.files_to_cols: Dict[str, int] = {elem: idx for idx, elem in enumerate(list("abcdefgh"))}
        self.cols_to_files: Dict[int, str] = {val: key for key, val in self.files_to_cols.items()}

    def print(self) -> None:
        """Prints the board matrix."""

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
        """Gets a fresh board to start a chess game."""

        return \
            [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
             ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
             ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

    def draw(self, screen: pygame.surface.Surface):
        """Draws the current state of the chess board on a pygame screen."""

        self._draw_board(screen)
        self._draw_pieces(screen)

    def make_move(self, from_square: Tuple[int, int], to_square: Tuple[int, int]):
        """Moves a piece from source to destination square."""
        from_row, from_col = from_square
        to_row, to_col = to_square

        piece_to_move = self.board[from_row][from_col]
        # piece_to_be_captured = self.board[to_row][to_col]

        self.board[from_row][from_col] = "--"
        self.board[to_row][to_col] = piece_to_move

        move_made = self._get_square_name(from_row, from_col) + self._get_square_name(to_row, to_col)
        self.move_log.append(move_made)
        self.white_to_move = not self.white_to_move

    def _get_square_name(self, row: int, col: int) -> str:
        """Gets square name in chess notation for a given row and column."""
        return self.cols_to_files[col] + self.rows_to_ranks[row]


def main():
    b = Board()
    b.print()


if __name__ == '__main__':
    main()
