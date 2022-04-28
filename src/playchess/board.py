import copy
from pprint import pprint
from typing import List, Dict, Tuple

from playchess.piece import Piece


class Board:
    """
    Class to represent a chess board.
    """

    def __init__(self):
        self.board: List[List[Piece]] = self._get_fresh_board_()

        # Mappings between notation and board matrix positions
        self.ranks_to_rows: Dict[str, int] = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
        self.rows_to_ranks: Dict[int, str] = {val: key for key, val in self.ranks_to_rows.items()}
        print(self.rows_to_ranks)
        self.files_to_cols: Dict[str, int] = {elem: idx for idx, elem in enumerate(list("abcdefgh"))}
        self.cols_to_files: Dict[int, str] = {val: key for key, val in self.files_to_cols.items()}
        self.white_king_location: Tuple[int, int] = (7, 4)
        self.black_king_location: Tuple[int, int] = (0, 4)

    def print(self) -> None:
        """Prints the board matrix."""

        for row in self.board:
            pprint([piece.value for piece in row])

    @staticmethod
    def _get_fresh_board_() -> List[List[Piece]]:
        """Gets a fresh board to start a chess game."""

        return \
            [[Piece.BLACK_ROOK, Piece.BLACK_KNIGHT, Piece.BLACK_BISHOP, Piece.BLACK_QUEEN,
              Piece.BLACK_KING, Piece.BLACK_BISHOP, Piece.BLACK_KNIGHT, Piece.BLACK_ROOK],
             [Piece.BLACK_PAWN, Piece.BLACK_PAWN, Piece.BLACK_PAWN, Piece.BLACK_PAWN,
              Piece.BLACK_PAWN, Piece.BLACK_PAWN, Piece.BLACK_PAWN, Piece.BLACK_PAWN],
             [Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE],
             [Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE],
             [Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE],
             [Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE, Piece.NONE],
             [Piece.WHITE_PAWN, Piece.WHITE_PAWN, Piece.WHITE_PAWN, Piece.WHITE_PAWN,
              Piece.WHITE_PAWN, Piece.WHITE_PAWN, Piece.WHITE_PAWN, Piece.WHITE_PAWN],
             [Piece.WHITE_ROOK, Piece.WHITE_KNIGHT, Piece.WHITE_BISHOP, Piece.WHITE_QUEEN,
              Piece.WHITE_KING, Piece.WHITE_BISHOP, Piece.WHITE_KNIGHT, Piece.WHITE_ROOK]]

    def get_square_name(self, row: int, col: int) -> str:
        """Gets square name in chess notation for a given row and column."""
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def __getitem__(self, item: int):
        return self.board[item]

    def is_empty_square(self, row: int, col: int) -> bool:
        """Checks if a given square is empty."""

        return True if self.board[row][col].is_none() else False

    def clear_square(self, row: int, col: int) -> None:
        """Empties a square."""

        self.board[row][col] = Piece.NONE

    def update_square(self, row: int, col: int, piece: Piece) -> None:
        """Updates a square to a given piece."""

        self.board[row][col] = piece

    def __iter__(self):
        for row in self.board:
            yield row

    def reset(self):
        """Resets the board."""

        self.board = self._get_fresh_board_()
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)

    def deep_copy(self):
        """Returns a deep copy of the board."""

        return copy.deepcopy(self)


def main():
    b = Board()
    b.print()


if __name__ == '__main__':
    main()
