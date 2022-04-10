from typing import List, Tuple, Union

import pygame
from playchess.board import Board
from playchess.config import WIDTH, HEIGHT, BACKGROUND_COLOUR, SQUARE_SIZE, MAX_FPS
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
    chess_board = Board()
    game = Game(chess_board)

    move_making_clicks: List[Tuple[int, int]] = []
    selected_square: Union[Tuple[int, int], None] = None

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                break

            elif e.type == pygame.MOUSEBUTTONDOWN:

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
                    move = Move(move_making_clicks[0], move_making_clicks[1], chess_board)
                    game.make_move(move)
                    selected_square = None
                    move_making_clicks.clear()
                    # chess_board.print()

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_u:
                    game.undo_move()

        clock.tick(MAX_FPS)
        pygame.display.flip()
        game.draw(screen)


if __name__ == '__main__':
    play()
