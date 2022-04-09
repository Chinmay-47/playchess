from typing import Tuple

from playchess.board import Board


class Move:
    """Class to represent a chess move."""

    def __init__(self, from_square: Tuple[int, int], to_square: Tuple[int, int], board: Board):
        self.from_square = from_square
        self.to_square = to_square
        self.chess_board = board
        self.from_row, self.from_col = self.from_square
        self.to_row, self.to_col = self.to_square
        self.from_square_name = self.chess_board.get_square_name(self.from_row, self.from_col)
        self.to_square_name = self.chess_board.get_square_name(self.to_row, self.to_col)
        self.piece_moved = self.chess_board[self.from_row][self.from_col]
        self.piece_captured = self.chess_board[self.to_row][self.to_col]

        self.piece_is_captured = True
        if self.chess_board.is_empty_square(self.to_row, self.to_col):
            self.piece_is_captured = False

    def __str__(self):
        if not self.piece_is_captured:
            return self.piece_moved + self.from_square_name + self.to_square_name

        return self.piece_moved + self.from_square_name + "x" + self.piece_captured + self.to_square_name

    @property
    def name(self):
        return self.__str__()


def main():
    m = Move((6, 3), (4, 3), Board())
    print(m.name)


if __name__ == '__main__':
    main()
