"""
Loads all Images of the chess pieces into a global dictionary.
"""


import os
from typing import Dict

import pygame
from playchess.config import SQUARE_SIZE
from pygame import Surface


CHESS_PIECE_IMAGES: Dict[str, Surface] = {}

IMAGES_DIR_PATH: str = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

for img_file in os.listdir(IMAGES_DIR_PATH):
    if not img_file.endswith(".png"):
        continue
    piece = img_file.split('.')[0]
    loaded_image = pygame.image.load(IMAGES_DIR_PATH + os.sep + img_file)
    CHESS_PIECE_IMAGES[piece] = pygame.transform.scale(loaded_image, (SQUARE_SIZE, SQUARE_SIZE))
