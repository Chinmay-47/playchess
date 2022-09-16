"""
Configuration settings for playchess.
"""


BOARD_WIDTH = BOARD_HEIGHT = 512     # Width and Height of the chess board

DIMENSIONS = 8  # Chess board is 8x8

SQUARE_SIZE = BOARD_HEIGHT // DIMENSIONS  # Size of each square

MAX_FPS = 15    # For Animations

BACKGROUND_COLOUR = "white"     # Background color of the board

LIGHT_SQUARE_COLOUR = "white"   # Colour of light squares

DARK_SQUARE_COLOUR = "gray"   # Colour of light squares

SELECTED_SQUARE_COLOUR = "blue"     # Colour of selected square

SELECTED_SQUARE_ALPHA = 100         # Transparency of selected square colour (0 = transparent -> 255 = opaque)

MOVABLE_SQUARE_COLOUR = "yellow"    # Colour of squares to which selected piece can be moved

MOVABLE_SQUARE_ALPHA = 100         # Transparency of movable squares colour (0 = transparent -> 255 = opaque)

END_GAME_FONT_COLOUR = "black"      # Colour of the game over text

END_GAME_FONT_SIZE = 32             # Size of game over text

BLACK_WINS_TEXT = "Black wins by Checkmate!"

WHITE_WINS_TEXT = "White wins by Checkmate!"

STALEMATE_TEXT = "Stalemate!"

MOVE_LOG_PANEL_WIDTH = 250

MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT

MOVE_LOG_PANEL_BACKGROUND_COLOUR = "black"

MOVE_LOG_FONT_SIZE = 12

MOVE_LOG_FONT_COLOUR = "white"
