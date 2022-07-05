import pygame
from playchess.config import WIDTH, HEIGHT, END_GAME_FONT_COLOUR, END_GAME_FONT_SIZE


def draw_game_over_text(screen: pygame.surface.Surface, text: str) -> None:
    """Draws text onto a pygame screen."""

    font = pygame.font.Font(pygame.font.get_default_font(), END_GAME_FONT_SIZE)
    text_obj = font.render(text, False, pygame.Color(END_GAME_FONT_COLOUR))

    text_loc_width = WIDTH/2 - text_obj.get_width()/2
    text_loc_height = HEIGHT/2 - text_obj.get_height()/2
    text_loc = pygame.Rect(0, 0, WIDTH, HEIGHT).move(text_loc_width, text_loc_height)
    screen.blit(text_obj, text_loc)
