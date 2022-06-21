from typing import List, Tuple, Union

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
    # [print(item) for item in valid_moves]
    # print("#" * 50)
    board_state_changed: bool = False
    game_over: bool = False

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit(0)

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    continue

                # (x, y) location of mouse click
                click_location = pygame.mouse.get_pos()
                selected_col = click_location[0] // SQUARE_SIZE
                selected_row = click_location[1] // SQUARE_SIZE

                # If already selected square is selected, clear move_making_clicks and selected_square
                if selected_square == (selected_row, selected_col):
                    selected_square = None
                    move_making_clicks = []
                else:
                    selected_square = (selected_row, selected_col)
                    move_making_clicks.append(selected_square)  # Append both clicks

                if len(move_making_clicks) == 2:    # After second click
                    move = Move(move_making_clicks[0], move_making_clicks[1], game.chess_board)

                    for valid_move in valid_moves:
                        if valid_move == move:
                            game.make_move(valid_move)
                            board_state_changed = True
                            break
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
            # [print(item) for item in valid_moves]
            # print("#" * 50)
            board_state_changed = False

        game_over = True if game.check_mate or game.stale_mate else False
        if game.check_mate and game.turn.is_white():
            draw_text(screen, BLACK_WINS_TEXT)
        elif game.check_mate and not game.turn.is_white():
            draw_text(screen, WHITE_WINS_TEXT)
        elif game.stale_mate:
            draw_text(screen, STALEMATE_TEXT)

        clock.tick(MAX_FPS)
        pygame.display.flip()
        game.draw(screen, selected_square, valid_moves)


if __name__ == '__main__':
    play()
