from typing import Tuple

from playchess.board import Board


class Move:
    """Class to represent a chess move."""

    def __init__(self, from_square: Tuple[int, int], to_square: Tuple[int, int], board: Board, *,
                 is_en_passant: bool = False, is_castle: bool = False):

        self.from_square = from_square
        self.to_square = to_square
        self.from_row, self.from_col = self.from_square
        self.to_row, self.to_col = self.to_square

        # self.chess_board = board.deep_copy()
        self.chess_board = board

        self.piece_moved = self.chess_board[self.from_row][self.from_col]
        self.piece_captured = self.chess_board[self.to_row][self.to_col]

        # Pawn promotion
        self.is_white_pawn_promotion = self.piece_moved.is_white() and self.piece_moved.is_pawn() and self.to_row == 0
        self.is_black_pawn_promotion = self.piece_moved.is_black() and self.piece_moved.is_pawn() and self.to_row == 7
        self.is_pawn_promotion = self.is_white_pawn_promotion or self.is_black_pawn_promotion

        # En-passant
        self.is_en_passant = is_en_passant
        if self.is_en_passant:
            self.piece_captured = self.chess_board[self.from_row][self.to_col]

        self.piece_is_captured = True
        if self.chess_board.is_empty_square(self.to_row, self.to_col):
            self.piece_is_captured = False

        # Castling
        self.is_castle = is_castle

        self.from_square_name = self.chess_board.get_square_name(self.from_row, self.from_col)
        self.to_square_name = self.chess_board.get_square_name(self.to_row, self.to_col)

    def __str__(self):
        if not self.piece_is_captured:
            return self.piece_moved.value + self.from_square_name + self.to_square_name

        return self.piece_moved.value + self.from_square_name + "x" + self.piece_captured.value + self.to_square_name

    @property
    def name(self):
        return self.__str__()

    @property
    def move_log_name(self):

        if self.is_castle:
            return "O-O" if self.to_col == 6 else "O-O-O"

        if not self.piece_is_captured:
            return self.from_square_name + self.to_square_name

        return self.from_square_name + "x" + self.to_square_name

    def __eq__(self, other):
        return self.name == other.name


def main():
    m = Move((6, 3), (4, 3), Board())
    print(m.name)


if __name__ == '__main__':
    main()
