from typing import List, Optional

import pygame
from playchess.board import Board
from playchess.config import SQUARE_SIZE, DIMENSIONS, LIGHT_SQUARE_COLOUR, DARK_SQUARE_COLOUR
from playchess.images import CHESS_PIECE_IMAGES
from playchess.move import Move
from playchess.piece import Piece
from playchess.turn import Turn


class Game:
    """
    Class to represent a chess game.
    """

    def __init__(self, chess_board: Board):
        self.chess_board = chess_board
        self.move_log: List[Move] = []
        self.turn: Turn = Turn.WHITE

    def _draw_board_pieces(self, screen: pygame.surface.Surface):
        """Draws the chess pieces according to the board state."""

        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):

                # Ignore empty squares
                if self.chess_board.is_empty_square(row, col):
                    continue

                piece = self.chess_board[row][col]
                screen.blit(CHESS_PIECE_IMAGES[piece.value], pygame.Rect(col * SQUARE_SIZE,
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
        """Makes a chess move."""

        # Does not work for castling, en-passant and pawn promotion
        self.chess_board.clear_square(move.from_row, move.from_col)
        self.chess_board.update_square(move.to_row, move.to_col, move.piece_moved)
        self.move_log.append(move)
        self.change_turn()

    def change_turn(self):
        """Changes the turns of the game."""

        self.turn = Turn.BLACK if self.turn.is_white() else Turn.WHITE

    def undo_move(self):
        """Undo a last made move."""

        if len(self.move_log) > 0:
            move = self.move_log.pop()
            self.chess_board.update_square(move.from_row, move.from_col, move.piece_moved)
            self.chess_board.update_square(move.to_row, move.to_col, move.piece_captured)
            self.change_turn()

    def get_valid_moves(self) -> List[Move]:
        return self._get_all_possible_moves()   # Not considering checks for now

    def _get_all_possible_moves(self) -> List[Move]:
        """Generate all currently possible moves without considering checks."""

        possible_moves: List[Move] = []
        for row_no, row in enumerate(self.chess_board):
            for col_no, piece in enumerate(self.chess_board[row_no]):

                # This condition also ensures that empty squares cannot be moved
                white_moving_white = piece.is_white() and self.turn.is_white()
                black_moving_black = piece.is_black() and not self.turn.is_white()
                if not (white_moving_white or black_moving_black):
                    continue

                possible_moves.extend(self._get_all_piece_moves(row_no, col_no, piece))

        return possible_moves

    def _get_all_pawn_moves(self, row: int, col: int) -> List[Move]:
        """Get all possible moves for a pawn on a given row and column."""

        moves: List[Move] = []

        # White Advances
        if self.turn.is_white() and self.chess_board.is_empty_square(row-1, col):  # 1 square advance
            moves.append(Move((row, col), (row-1, col), self.chess_board))
            if self.chess_board.is_empty_square(row-2, col):  # 2 square advance
                moves.append(Move((row, col), (row-2, col), self.chess_board))

        # White Captures Left
        if self.turn.is_white() and col-1 >= 0 and self.chess_board[row-1][col-1].is_black():
            moves.append(Move((row, col), (row-1, col-1), self.chess_board))

        # White Captures Right
        if self.turn.is_white() and col+1 <= 7 and self.chess_board[row-1][col+1].is_black():
            moves.append(Move((row, col), (row-1, col+1), self.chess_board))

        # Black Advances
        if not self.turn.is_white() and self.chess_board.is_empty_square(row+1, col):  # 1 square advance
            moves.append(Move((row, col), (row+1, col), self.chess_board))
            if self.chess_board.is_empty_square(row+2, col):  # 2 square advance
                moves.append(Move((row, col), (row+2, col), self.chess_board))

        # Black Captures Left
        if not self.turn.is_white() and col+1 <= 7 and self.chess_board[row+1][col+1].is_white():
            moves.append(Move((row, col), (row+1, col+1), self.chess_board))

        # Black Captures Right
        if not self.turn.is_white() and col-1 >= 0 and self.chess_board[row+1][col-1].is_white():
            moves.append(Move((row, col), (row+1, col-1), self.chess_board))

        return moves

    def _get_all_rook_moves(self, row: int, col: int) -> List[Move]:
        """Get all possible moves for a rook on a given row and column."""

    def _get_all_knight_moves(self, row: int, col: int) -> List[Move]:
        """Get all possible moves for a knight on a given row and column."""

    def _get_all_bishop_moves(self, row: int, col: int) -> List[Move]:
        """Get all possible moves for a bishop on a given row and column."""

    def _get_all_queen_moves(self, row: int, col: int) -> List[Move]:
        """Get all possible moves for a queen on a given row and column."""

    def _get_all_king_moves(self, row: int, col: int) -> List[Move]:
        """Get all possible moves for a king on a given row and column."""

    def _get_all_piece_moves(self, row: int, col: int, piece: Piece):
        """Get all possible moves for a given piece on a row and col"""

        if piece.is_pawn():
            return self._get_all_pawn_moves(row, col)
        if piece.is_rook():
            return self._get_all_rook_moves(row, col)
        if piece.is_knight():
            return self._get_all_knight_moves(row, col)
        if piece.is_bishop():
            return self._get_all_bishop_moves(row, col)
        if piece.is_queen():
            return self._get_all_queen_moves(row, col)
        if piece.is_king():
            return self._get_all_king_moves(row, col)


def main():
    g = Game(Board())
    print(g.game_sequence)


if __name__ == '__main__':
    main()
