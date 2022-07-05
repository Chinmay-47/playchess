from typing import List, Tuple, Union

import pygame
from playchess._utils import draw_game_over_text
from playchess.board import Board
from playchess.config import (WIDTH, HEIGHT, BACKGROUND_COLOUR, SQUARE_SIZE, MAX_FPS,
                              BLACK_WINS_TEXT, WHITE_WINS_TEXT, STALEMATE_TEXT)
from playchess.game import Game
from playchess.move import Move
from playchess.move_finder import (RandomMoveFinder, MaterialMoveFinder, MinMaxMoveFinder, PrunedMinMaxMoveFinder)

AI_MOVE_FINDERS = {"random": RandomMoveFinder,
                   "material": MaterialMoveFinder,
                   "minmax": MinMaxMoveFinder,
                   "minmax_pruned": PrunedMinMaxMoveFinder}


def play(player1: str = "human", player2: str = "bot", ai: str = "minmax_pruned", depth: int = 2):
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

    human_plays_white: bool = True if player1 == "human" else False
    human_plays_black: bool = True if player2 == "human" else False

    while True:
        human_turn = (game.turn.is_white() and human_plays_white) or \
                     (not game.turn.is_white() and human_plays_black)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit(0)

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if game_over or not human_turn:
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

                if len(move_making_clicks) == 2:  # After second click
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
            board_state_changed = False

        game_over = True if game.check_mate or game.stale_mate else False
        if game_over:
            _display_game_over_text(screen, game)

        clock.tick(MAX_FPS)
        pygame.display.flip()
        game.draw(screen, selected_square, valid_moves)

        # AI moves
        if not human_turn and not game_over:
            ai_move_finder = AI_MOVE_FINDERS[ai]
            if ai == "random":
                ai_move = ai_move_finder(valid_moves).find_move()
            elif ai == "material":
                ai_move = ai_move_finder(game, valid_moves).find_move()
            else:
                ai_move = ai_move_finder(game, valid_moves, depth).find_move()

            game.make_move(ai_move)
            board_state_changed = True


def _display_game_over_text(screen: pygame.surface.Surface, game_: Game):
    """Display game over text using game state."""

    if game_.check_mate and game_.turn.is_white():
        draw_game_over_text(screen, BLACK_WINS_TEXT)
    elif game_.check_mate and not game_.turn.is_white():
        draw_game_over_text(screen, WHITE_WINS_TEXT)
    elif game_.stale_mate:
        draw_game_over_text(screen, STALEMATE_TEXT)


if __name__ == '__main__':
    play(ai="minmax_pruned", depth=3)
