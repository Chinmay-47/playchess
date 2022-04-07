import pygame
from playchess.board import Board
from playchess.config import WIDTH, HEIGHT, BACKGROUND_COLOUR, MAX_FPS


def play():
    """
    Main driver to play the game.
    """

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color(BACKGROUND_COLOUR))
    chess_board = Board()
    chess_board.print()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                break

        clock.tick(MAX_FPS)
        pygame.display.flip()
        chess_board.draw(screen)


if __name__ == '__main__':
    play()
