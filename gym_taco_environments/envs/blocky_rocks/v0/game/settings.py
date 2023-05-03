from pathlib import Path

import pygame

from .src.frames import generate_frames

TILE_SIZE = 16
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 18

BASE_DIR = Path(__file__).parent

ENVIRONMENT = BASE_DIR / "env.txt"

# Graphics
GAME_TEXTURES = {
    "ground": pygame.image.load(BASE_DIR / "graphics" / "ground.png"),
    "rock": pygame.image.load(BASE_DIR / "graphics" / "rock.png"),
    "boulder": pygame.image.load(BASE_DIR / "graphics" / "boulder.png"),
    "miner": pygame.image.load(BASE_DIR / "graphics" / "miner.png"),
    "switch": pygame.image.load(BASE_DIR / "graphics" / "switch.png"),
    "hole": pygame.image.load(BASE_DIR / "graphics" / "hole.png"),
}

# Frames
GAME_FRAMES = {
    "ground": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "rock": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "boulder": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "hole": [pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)],
    "miner": generate_frames(
        GAME_TEXTURES["miner"], PLAYER_WIDTH, PLAYER_HEIGHT
    ),
}
