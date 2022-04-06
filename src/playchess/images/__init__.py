"""
Loads all Images of the chess pieces into a global dictionary.
"""


import os
from typing import Dict

import pygame
from pygame import Surface


CHESS_PIECE_IMAGES: Dict[str, Surface] = {}

IMAGES_DIR_PATH: str = "src" + os.sep + "playchess" + os.sep + "images"

for img_file in os.listdir(IMAGES_DIR_PATH):
    if not img_file.endswith(".png"):
        continue
    piece = img_file.split('.')[0]
    CHESS_PIECE_IMAGES[piece] = pygame.image.load(IMAGES_DIR_PATH + os.sep + img_file)
