import pathlib

import pygame

# Seeds for random number generation
SEED = 203853699

# Size of the square tiles used in this environment.
TILE_SIZE = 32

# Grid
ROWS = 16
COLS = 16

NUM_TILES = ROWS * COLS
NUM_ACTIONS = 4
INITIAL_STATE = 0

# Resolution to emulate
VIRTUAL_WIDTH = TILE_SIZE * COLS
VIRTUAL_HEIGHT = TILE_SIZE * ROWS

# Scale factor between virtual screen and window
H_SCALE = 4
V_SCALE = 4

# Resolution of the actual window
WINDOW_WIDTH = VIRTUAL_WIDTH * H_SCALE
WINDOW_HEIGHT = VIRTUAL_HEIGHT * V_SCALE

# Default pause time between steps (in seconds)
DEFAULT_DELAY = 0.5

BASE_DIR = pathlib.Path(__file__).parent

# Textures used in the environment
TEXTURES = {
    'tile': pygame.image.load(BASE_DIR / "assets" / "graphics" / "tile.png"),
    'battery': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery.png"),
    'character': [
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "el_reververo_left.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "el_reververo_right.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "el_reververo_left.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "el_reververo_right.png"),
    ]
}

# Initializing the mixer
pygame.mixer.init()

# Loading music
pygame.mixer.music.load(BASE_DIR / "assets" / "sounds" / "ice_village.ogg")

# Sound effects
SOUNDS = {
    'ice_cracking': pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "ice_cracking.ogg"),
    'win': pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "win.ogg")
}

P = {}