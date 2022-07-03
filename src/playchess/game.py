from copy import copy
from typing import List, Optional, Tuple

import pygame
from playchess._castling_rights import CastlingRights
from playchess.board import Board
from playchess.config import (SQUARE_SIZE, DIMENSIONS, LIGHT_SQUARE_COLOUR, DARK_SQUARE_COLOUR, SELECTED_SQUARE_COLOUR,
                              SELECTED_SQUARE_ALPHA, MOVABLE_SQUARE_COLOUR, MOVABLE_SQUARE_ALPHA)
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
        self.check_mate: bool = False
        self.stale_mate: bool = False
        self.en_passant_available: bool = True
        self.en_passant_to_square: Optional[Tuple[int, int]] = None
        self.castling_rights: CastlingRights = CastlingRights(True, True, True, True)
        self.castling_rights_log: List[CastlingRights] = [copy(self.castling_rights)]
        self.en_passant_to_square_log: List[Optional[Tuple[int, int]]] = [None]

    def __eq__(self, other):
        return self.game_sequence == other.game_sequence

    def __hash__(self):
        return hash(self.game_sequence)

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

    def highlight_selected_square(self, screen: pygame.surface.Surface, square: Optional[Tuple[int, int]]):
        """Highlights selected square."""

        if not square:
            return

        row, col = square
        piece = self.chess_board[row][col]

        white_moving_white = piece.is_white() and self.turn.is_white()
        black_moving_black = piece.is_black() and not self.turn.is_white()
        if not (white_moving_white or black_moving_black):
            return

        _new_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        _new_surface.set_alpha(SELECTED_SQUARE_ALPHA)
        _new_surface.fill(pygame.Color(SELECTED_SQUARE_COLOUR))
        screen.blit(_new_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    @staticmethod
    def highlight_valid_moves(screen: pygame.surface.Surface, square: Optional[Tuple[int, int]],
                              moves: List[Move]):
        """Highlights valid moves of a piece from a given square."""

        if not square:
            return

        for move in moves:
            if move.from_square != square:
                continue
            row, col = move.to_square
            _new_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            _new_surface.set_alpha(MOVABLE_SQUARE_ALPHA)
            _new_surface.fill(pygame.Color(MOVABLE_SQUARE_COLOUR))
            screen.blit(_new_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def draw(self, screen: pygame.surface.Surface, square: Optional[Tuple[int, int]], val_moves: List[Move]):
        """Draws the current state of the chess game on a pygame screen."""

        self._draw_board(screen)
        self.highlight_selected_square(screen, square)
        self.highlight_valid_moves(screen, square, val_moves)
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

        self.chess_board.clear_square(move.from_row, move.from_col)
        self.chess_board.update_square(move.to_row, move.to_col, move.piece_moved)

        # pawn promotion
        if move.is_white_pawn_promotion:
            self.chess_board.update_square(move.to_row, move.to_col, Piece.WHITE_QUEEN)
        elif move.is_black_pawn_promotion:
            self.chess_board.update_square(move.to_row, move.to_col, Piece.BLACK_QUEEN)

        # En-passant
        if move.is_en_passant:
            self.chess_board.clear_square(move.from_row, move.to_col)
            self.en_passant_available = False
            self.en_passant_to_square = None

        if self.en_passant_to_square is not None and self.en_passant_available and not move.is_en_passant:
            self.en_passant_to_square = None

        # Update en-passant square
        if move.piece_moved.is_pawn() and abs(move.from_row - move.to_row) == 2:
            self.en_passant_to_square = ((move.from_row + move.to_row)//2, move.from_col)

        if not move.piece_moved.is_pawn():
            self.en_passant_to_square = None

        # Keep track of the king
        if move.piece_moved.is_white() and move.piece_moved.is_king():
            self.chess_board.white_king_location = (move.to_row, move.to_col)
        elif move.piece_moved.is_black() and move.piece_moved.is_king():
            self.chess_board.black_king_location = (move.to_row, move.to_col)

        # Handle castling
        if move.is_castle:
            if move.to_col - move.from_col == 2:    # King side castle
                self.chess_board.update_square(move.to_row, move.to_col - 1,
                                               self.chess_board[move.to_row][move.to_col + 1])
                self.chess_board.clear_square(move.to_row, move.to_col + 1)

            else:   # Queen side castle
                self.chess_board.update_square(move.to_row, move.to_col + 1,
                                               self.chess_board[move.to_row][move.to_col - 2])
                self.chess_board.clear_square(move.to_row, move.to_col - 2)

        self.en_passant_to_square_log.append(self.en_passant_to_square)
        self.move_log.append(move)
        self.change_turn()

        self._update_castling_rights(move)
        self.castling_rights_log.append(copy(self.castling_rights))

    def change_turn(self):
        """Changes the turns of the game."""

        self.turn = Turn.BLACK if self.turn.is_white() else Turn.WHITE

    def undo_move(self):
        """Undo a last made move."""

        if len(self.move_log) > 0:
            move = self.move_log.pop()
            self.chess_board.update_square(move.from_row, move.from_col, move.piece_moved)

            if move.is_en_passant:
                self.chess_board.clear_square(move.to_row, move.to_col)
                self.chess_board.update_square(move.from_row, move.to_col, move.piece_captured)
                self.en_passant_available = True
            else:
                self.chess_board.update_square(move.to_row, move.to_col, move.piece_captured)

            # Update en-passant square
            self.en_passant_to_square_log.pop()
            self.en_passant_to_square = self.en_passant_to_square_log[-1]

            self.change_turn()

            # Keep track of the king
            if move.piece_moved.is_white() and move.piece_moved.is_king():
                self.chess_board.white_king_location = (move.from_row, move.from_col)
            elif move.piece_moved.is_black() and move.piece_moved.is_king():
                self.chess_board.black_king_location = (move.from_row, move.from_col)

            if move.is_castle:
                if move.to_col - move.from_col == 2:    # King side castle
                    self.chess_board.update_square(move.to_row, move.to_col + 1,
                                                   self.chess_board[move.to_row][move.to_col - 1])
                    self.chess_board.clear_square(move.to_row, move.to_col - 1)

                else:   # Queen side castle
                    self.chess_board.update_square(move.to_row, move.to_col - 2,
                                                   self.chess_board[move.to_row][move.to_col + 1])
                    self.chess_board.clear_square(move.to_row, move.to_col + 1)

            # Update castling rights
            self.castling_rights_log.pop()
            self.castling_rights = copy(self.castling_rights_log[-1])

    def _update_castling_rights(self, move: Move):
        """Updates the castling rights for a given move."""

        if move.piece_moved.is_king() and move.piece_moved.is_white():
            self.castling_rights.white_king_side = False
            self.castling_rights.white_queen_side = False
        elif move.piece_moved.is_king() and move.piece_moved.is_black():
            self.castling_rights.black_king_side = False
            self.castling_rights.black_queen_side = False
        elif move.piece_moved.is_white() and move.piece_moved.is_rook():
            if move.from_row == 7 and move.from_col == 0:       # Queen side rook
                self.castling_rights.white_queen_side = False
            elif move.from_row == 7 and move.from_col == 7:     # King side rook
                self.castling_rights.white_king_side = False
        elif move.piece_moved.is_black() and move.piece_moved.is_rook():
            if move.from_row == 0 and move.from_col == 0:       # Queen side rook
                self.castling_rights.white_queen_side = False
            elif move.from_row == 0 and move.from_col == 7:     # King side rook
                self.castling_rights.white_king_side = False

    def get_valid_moves(self) -> List[Move]:
        """Generates all the valid moves in a position."""

        valid_moves: List[Move] = []

        all_possible_moves = self._get_all_possible_moves()

        # Castling moves
        if self.turn.is_white():
            king_row, king_col = self.chess_board.white_king_location
        else:
            king_row, king_col = self.chess_board.black_king_location

        if not self.is_square_attacked(king_row, king_col):  # Cannot castle if checked

            # King side castling
            _king_side_castle = (self.turn.is_white() and self.castling_rights.white_king_side) or \
                                (not self.turn.is_white() and self.castling_rights.black_king_side)
            if _king_side_castle:
                all_possible_moves.extend(self._get_king_side_castling_moves(king_row, king_col))

            # Queen side castling
            _queen_side_castle = (self.turn.is_white() and self.castling_rights.white_queen_side) or \
                                 (not self.turn.is_white() and self.castling_rights.black_queen_side)
            if _queen_side_castle:
                all_possible_moves.extend(self._get_queen_side_castling_moves(king_row, king_col))

        # We need to keep track of this and reset it, as this value changes while generating valid moves
        temp_en_passant_to_square = self.en_passant_to_square

        # We check the validity of move by actually making the move.
        for move in all_possible_moves:
            self.make_move(move)

            # Make move function swaps turns, so we swap it back to see if making a move leaves the king checked
            self.change_turn()
            if not self.is_king_checked():
                valid_moves.append(move)

            self.change_turn()
            self.undo_move()

        if not valid_moves and self.is_king_checked():
            self.check_mate = True
        elif not valid_moves and not self.is_king_checked():
            self.stale_mate = True
        else:
            # We need to do this if the check mate move is then undone
            self.check_mate = False
            self.stale_mate = False

        self.en_passant_to_square = temp_en_passant_to_square

        return valid_moves

    def is_king_checked(self):
        """Checks if the king of current player is under check."""

        return (self.turn.is_white() and self._is_white_king_checked()) or \
               (not self.turn.is_white() and self._is_black_king_checked())

    def _is_white_king_checked(self):
        """Checks if the white king is under check."""

        return self.is_square_attacked(self.chess_board.white_king_location[0], self.chess_board.white_king_location[1])

    def _is_black_king_checked(self):
        """Checks if the black king is under check."""

        return self.is_square_attacked(self.chess_board.black_king_location[0], self.chess_board.black_king_location[1])

    def is_square_attacked(self, row: int, col: int) -> bool:
        """Checks if a given square is under attack by opponents moves in the next turn."""

        self.change_turn()
        opponent_moves = self._get_all_possible_moves()
        self.change_turn()

        for move in opponent_moves:
            if move.to_row == row and move.to_col == col:
                return True

        return False

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
        if self.turn.is_white() and self.chess_board.is_empty_square(row - 1, col):  # 1 square advance
            moves.append(Move((row, col), (row - 1, col), self.chess_board))
            if row == 6 and self.chess_board.is_empty_square(row - 2, col):  # 2 square advance
                moves.append(Move((row, col), (row - 2, col), self.chess_board))

        # White Captures Left
        if self.turn.is_white() and col - 1 >= 0 and self.chess_board[row - 1][col - 1].is_black():
            moves.append(Move((row, col), (row - 1, col - 1), self.chess_board))

        # White Captures Left (En-passant)
        if self.turn.is_white() and col - 1 >= 0 and self.chess_board.is_empty_square(row - 1, col - 1) and \
                (row - 1, col - 1) == self.en_passant_to_square and self.en_passant_available:
            moves.append(Move((row, col), (row - 1, col - 1), self.chess_board, is_en_passant=True))

        # White Captures Right
        if self.turn.is_white() and col + 1 <= 7 and self.chess_board[row - 1][col + 1].is_black():
            moves.append(Move((row, col), (row - 1, col + 1), self.chess_board))

        # White Captures Right (En-passant)
        if self.turn.is_white() and col + 1 <= 7 and self.chess_board.is_empty_square(row - 1, col + 1) and \
                (row - 1, col + 1) == self.en_passant_to_square and self.en_passant_available:
            moves.append(Move((row, col), (row - 1, col + 1), self.chess_board, is_en_passant=True))

        # Black Advances
        if not self.turn.is_white() and self.chess_board.is_empty_square(row + 1, col):  # 1 square advance
            moves.append(Move((row, col), (row + 1, col), self.chess_board))
            if row == 1 and self.chess_board.is_empty_square(row + 2, col):  # 2 square advance
                moves.append(Move((row, col), (row + 2, col), self.chess_board))

        # Black Captures Left
        if not self.turn.is_white() and col + 1 <= 7 and self.chess_board[row + 1][col + 1].is_white():
            moves.append(Move((row, col), (row + 1, col + 1), self.chess_board))

        # Black Captures Left (En-passant)
        if not self.turn.is_white() and col + 1 <= 7 and self.chess_board.is_empty_square(row + 1, col + 1) and \
                (row + 1, col + 1) == self.en_passant_to_square and self.en_passant_available:
            moves.append(Move((row, col), (row + 1, col + 1), self.chess_board, is_en_passant=True))

        # Black Captures Right
        if not self.turn.is_white() and col - 1 >= 0 and self.chess_board[row + 1][col - 1].is_white():
            moves.append(Move((row, col), (row + 1, col - 1), self.chess_board))

        # Black Captures Right (En-passant)
        if not self.turn.is_white() and col - 1 >= 0 and self.chess_board.is_empty_square(row + 1, col - 1) and \
                (row + 1, col - 1) == self.en_passant_to_square and self.en_passant_available:
            moves.append(Move((row, col), (row + 1, col - 1), self.chess_board, is_en_passant=True))

        return moves

    def _get_all_rook_moves(self, row: int, col: int) -> List[Move]:
        """Get all possible moves for a rook on a given row and column."""

        moves: List[Move] = []

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Up, Left, Down, Right

        # Check 7 squares in 4 directions for valid rook moves
        for direction in directions:
            for i in range(1, 8):

                to_row = row + direction[0] * i
                to_col = col + direction[1] * i

                if not 0 <= to_row < 8 or not 0 <= to_col < 8:  # Out of board (stop searching)
                    break

                if self.chess_board.is_empty_square(to_row, to_col):    # Empty square is valid move (keep searching)
                    moves.append(Move((row, col), (to_row, to_col), self.chess_board))
                    continue

                valid_black_enemy = self.turn.is_white() and self.chess_board[to_row][to_col].is_black()
                valid_white_enemy = not self.turn.is_white() and self.chess_board[to_row][to_col].is_white()

                if not (valid_black_enemy or valid_white_enemy):  # Friendly piece invalid (stop searching)
                    break

                # Capturing opposite colour is valid (stop searching)
                moves.append(Move((row, col), (to_row, to_col), self.chess_board))
                break

        return moves

    def _get_all_knight_moves(self, row: int, col: int) -> List[Move]:
        """Get all possible moves for a knight on a given row and column."""

        moves: List[Move] = []

        # Knight can move to 8 squares from a given square
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for move in knight_moves:

            to_row = row + move[0]
            to_col = col + move[1]

            if not 0 <= to_row < 8 or not 0 <= to_col < 8:  # Out of board (skip to next)
                continue

            friendly_white = self.turn.is_white() and self.chess_board[to_row][to_col].is_white()
            friendly_black = not self.turn.is_white() and self.chess_board[to_row][to_col].is_black()

            # This condition also ensures that knight can move to empty squares
            if friendly_black or friendly_white:
                continue

            moves.append(Move((row, col), (to_row, to_col), self.chess_board))

        return moves

    def _get_all_bishop_moves(self, row: int, col: int) -> List[Move]:
        """Get all possible moves for a bishop on a given row and column."""

        moves: List[Move] = []

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonals

        # Check 7 squares in 4 directions for valid bishop moves
        for direction in directions:
            for i in range(1, 8):

                to_row = row + direction[0] * i
                to_col = col + direction[1] * i

                if not 0 <= to_row < 8 or not 0 <= to_col < 8:  # Out of board (stop searching)
                    break

                if self.chess_board.is_empty_square(to_row, to_col):  # Empty square is valid move (keep searching)
                    moves.append(Move((row, col), (to_row, to_col), self.chess_board))
                    continue

                valid_black_enemy = self.turn.is_white() and self.chess_board[to_row][to_col].is_black()
                valid_white_enemy = not self.turn.is_white() and self.chess_board[to_row][to_col].is_white()

                if not (valid_black_enemy or valid_white_enemy):  # Friendly piece invalid (stop searching)
                    break

                # Capturing opposite colour is valid (stop searching)
                moves.append(Move((row, col), (to_row, to_col), self.chess_board))
                break

        return moves

    def _get_all_queen_moves(self, row: int, col: int) -> List[Move]:
        """Get all possible moves for a queen on a given row and column."""

        queen_diagonal_moves = self._get_all_bishop_moves(row, col)
        queen_straight_moves = self._get_all_rook_moves(row, col)

        return queen_diagonal_moves + queen_straight_moves

    def _get_all_king_moves(self, row: int, col: int) -> List[Move]:
        """Get all possible moves for a king on a given row and column."""

        moves: List[Move] = []

        # King can move to 8 squares from a given square
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for move in king_moves:

            to_row = row + move[0]
            to_col = col + move[1]

            if not 0 <= to_row < 8 or not 0 <= to_col < 8:  # Out of board (skip to next)
                continue

            friendly_white = self.turn.is_white() and self.chess_board[to_row][to_col].is_white()
            friendly_black = not self.turn.is_white() and self.chess_board[to_row][to_col].is_black()

            # This condition also ensures that king can move to empty squares
            if friendly_black or friendly_white:
                continue

            moves.append(Move((row, col), (to_row, to_col), self.chess_board))

        return moves

    def _get_king_side_castling_moves(self, row: int, col: int) -> List[Move]:
        """Get king side castling moves."""

        moves: List[Move] = []

        if (self.chess_board.is_empty_square(row, col + 1) and self.chess_board.is_empty_square(row, col + 2)) and \
                (not self.is_square_attacked(row, col + 1) and not self.is_square_attacked(row, col + 2)):
            moves.append((Move((row, col), (row, col + 2), self.chess_board, is_castle=True)))

        return moves

    def _get_queen_side_castling_moves(self, row: int, col: int) -> List[Move]:
        """Get queen side castling moves."""

        moves: List[Move] = []

        if (self.chess_board.is_empty_square(row, col - 1) and
            self.chess_board.is_empty_square(row, col - 2) and
            self.chess_board.is_empty_square(row, col - 3)) and \
                (not self.is_square_attacked(row, col - 1) and
                 not self.is_square_attacked(row, col - 2)):
            moves.append((Move((row, col), (row, col - 2), self.chess_board, is_castle=True)))

        return moves

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
