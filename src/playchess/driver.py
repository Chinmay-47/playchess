from typing import List, Tuple, Union, Optional

import pygame
from playchess._utils import draw_text
from playchess.board import Board
from playchess.config import (WIDTH, HEIGHT, BACKGROUND_COLOUR, SQUARE_SIZE, MAX_FPS,
                              BLACK_WINS_TEXT, WHITE_WINS_TEXT, STALEMATE_TEXT)
from playchess.game import Game
from playchess.move import Move


def play():
    """
    Main driver to play the game.
    """

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color(BACKGROUND_COLOUR))
    game = Game(Board())

    move_making_clicks: List[Tuple[int, int]] = []
    selected_square: Union[Tuple[int, int], None] = None

    valid_moves = game.get_valid_moves()

    board_state_changed: bool = False
    game_over: bool = False

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit(0)

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    continue

                selected_square, move_making_clicks, move = _handle_user_click(selected_square,
                                                                               move_making_clicks,
                                                                               game.chess_board)

                if move is not None and move in valid_moves:
                    game.make_move(move)
                    board_state_changed = True
                    selected_square = None
                    move_making_clicks.clear()

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_u:     # click 'u' to undo move
                    game.undo_move()
                    board_state_changed = True

                elif e.key == pygame.K_r:   # click 'r' to reset game
                    game = Game(Board())
                    valid_moves = game.get_valid_moves()
                    move_making_clicks = []
                    selected_square = None
                    board_state_changed = False

                elif e.key == pygame.K_q:   # click 'q' to quit game
                    quit(0)

        if board_state_changed:
            valid_moves = game.get_valid_moves()
            board_state_changed = False

        game_over = True if game.check_mate or game.stale_mate else False
        if game_over:
            _display_game_over_text(screen, game)

        clock.tick(MAX_FPS)
        pygame.display.flip()
        game.draw(screen, selected_square, valid_moves)


def _handle_user_click(prev_sel_square: Union[Tuple[int, int], None], move_clicks: List[Tuple[int, int]],
                       board: Board) -> Tuple[Union[Tuple[int, int], None], List[Tuple[int, int]], Optional[Move]]:
    """Handles a user click event in pygame and returns selected square, move making clicks and move to make."""

    move: Optional[Move] = None

    # (x, y) location of mouse click
    click_location = pygame.mouse.get_pos()
    selected_col = click_location[0] // SQUARE_SIZE
    selected_row = click_location[1] // SQUARE_SIZE

    # If already selected square is selected, clear move_making_clicks and selected_square
    if prev_sel_square == (selected_row, selected_col):
        square_selected = None
        move_clicks = []
    else:
        square_selected = (selected_row, selected_col)
        move_clicks.append(square_selected)  # Append both clicks

    if len(move_clicks) == 2:  # After second click
        move = Move(move_clicks[0], move_clicks[1], board)

    return square_selected, move_clicks, move


def _display_game_over_text(screen: pygame.surface.Surface, game_: Game):
    """Display game over text using game state."""

    if game_.check_mate and game_.turn.is_white():
        draw_text(screen, BLACK_WINS_TEXT)
    elif game_.check_mate and not game_.turn.is_white():
        draw_text(screen, WHITE_WINS_TEXT)
    elif game_.stale_mate:
        draw_text(screen, STALEMATE_TEXT)


if __name__ == '__main__':
    play()
