from pprint import pprint
from typing import List, Dict

from playchess.config import DIMENSIONS


class Board:
    """
    Class to represent a chess board.
    """

    def __init__(self):
        self.board: List[List[str]] = self._get_fresh_board_()

        # Mappings between notation and board matrix positions
        self.ranks_to_rows: Dict[str, int] = {str(i + 1): DIMENSIONS - 1 - i for i in range(DIMENSIONS)}
        self.rows_to_ranks: Dict[int, str] = {val: key for key, val in self.ranks_to_rows.items()}
        self.files_to_cols: Dict[str, int] = {elem: idx for idx, elem in enumerate(list("abcdefgh"))}
        self.cols_to_files: Dict[int, str] = {val: key for key, val in self.files_to_cols.items()}

    def print(self) -> None:
        """Prints the board matrix."""

        pprint(self.board)

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

    def get_square_name(self, row: int, col: int) -> str:
        """Gets square name in chess notation for a given row and column."""
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def __getitem__(self, item: int):
        return self.board[item]

    def is_empty_square(self, row: int, col: int) -> bool:
        """Checks if a given square is empty."""

        return self.board[row][col] == "--"

    def clear_square(self, row: int, col: int) -> None:
        """Empties a square."""

        self.board[row][col] = "--"

    def update_square(self, row: int, col: int, piece: str) -> None:
        """Updates a square to a given piece."""

        self.board[row][col] = piece


def main():
    b = Board()
    b.print()


if __name__ == '__main__':
    main()
