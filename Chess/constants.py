import pygame

# Screen dimensions
WIDTH = 1100
HEIGHT = 800
BOARD_SIZE = 800
SQUARE_SIZE = BOARD_SIZE // 8

# Colors
LIGHT_SQUARE = (240, 217, 181)  # #F0D9B5
DARK_SQUARE = (181, 136, 99)    # #B58863
HIGHLIGHT_COLOR = (123, 145, 59, 128)  # Semi-transparent green
VALID_MOVE_COLOR = (0, 0, 0, 40)       # Semi-transparent circle
LAST_MOVE_COLOR = (246, 246, 105, 128) # Semi-transparent yellow

# UI Colors
BG_COLOR = (30, 30, 30)
PANEL_COLOR = (45, 45, 45)
TEXT_COLOR = (220, 220, 220)
ACCENT_COLOR = (0, 150, 255)

# Piece Values
PIECE_VALUES = {
    'p': 100,
    'n': 320,
    'b': 330,
    'r': 500,
    'q': 900,
    'k': 20000
}

# Fonts
pygame.font.init()
FONT_MAIN = pygame.font.SysFont('Segoe UI', 32, bold=True)
FONT_SIDE = pygame.font.SysFont('Segoe UI', 24)
FONT_TINY = pygame.font.SysFont('Segoe UI', 16)
