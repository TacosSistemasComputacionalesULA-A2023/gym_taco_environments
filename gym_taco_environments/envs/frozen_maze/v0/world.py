import pygame

from . import settings
import math
from .tilemap import TileMap


class World:
    def __init__(self, title, state, action, render_mode):
        self.render_mode = render_mode
        if self.render_mode == 'human':
            pygame.init()
            pygame.display.init()
            pygame.mixer.music.play(loops=-1)
            self.render_surface = pygame.Surface(
                (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
            )
            self.screen = pygame.display.set_mode(
                (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
            )
            pygame.display.set_caption(title)
        self.current_state = state
        self.current_action = action
        self.render_character = True
        self.render_goal = True
        self.tilemap = None
        self.finish_state = None
        self._create_tilemap()

    def _create_tilemap(self):
        tile_texture_names = []
        
        for tile_num in range(settings.NUM_TILES):
            if settings.MAZE[math.floor(tile_num/settings.COLS)][tile_num % settings.COLS] == 'w':
                tile_texture_names.append("tile")
            else:
                tile_texture_names.append("ice")

        for _, actions_table in settings.P.items():
            for _, possibilities in actions_table.items():
                for _, state, reward, terminated in possibilities:
                    if terminated:
                        if reward > 0:
                            self.finish_state = state
                        else:
                            tile_texture_names[state] = "hole"

        tile_texture_names[self.finish_state] = "ice"
        self.tilemap = TileMap(tile_texture_names)

    def reset(self, state, action):
        self.state = state
        self.action = action
        self.render_character = True
        self.render_goal = True
        for tile in self.tilemap.tiles:
            if tile.texture_name == "cracked_hole":
                tile.texture_name = "hole"

    def update(self, state, action, reward, terminated):
        if terminated:
            if state == self.finish_state:
                self.render_goal = False
                if self.render_mode == 'human':
                    settings.SOUNDS['win'].play()
                    pass
            else:
                self.tilemap.tiles[state].texture_name = "cracked_hole"
                self.render_character = False
                if self.render_mode == 'human':
                    settings.SOUNDS['ice_cracking'].play()
                    settings.SOUNDS['water_splash'].play()
                    pass

        self.state = state
        self.action = action

    def render(self, render_mode):
        if render_mode != 'human':
            return

        self.render_surface.fill((0, 0, 0))

        self.tilemap.render(self.render_surface)

        self.render_surface.blit(
            settings.TEXTURES['stool'],
            (self.tilemap.tiles[0].x, self.tilemap.tiles[0].y)
        )

        if self.render_goal:
            self.render_surface.blit(
                settings.TEXTURES['goal'],
                (self.tilemap.tiles[self.finish_state].x,
                 self.tilemap.tiles[self.finish_state].y)
            )

        if self.render_character:
            self.render_surface.blit(
                settings.TEXTURES['character'][self.action],
                (self.tilemap.tiles[self.state].x,
                 self.tilemap.tiles[self.state].y)
            )

        self.screen.blit(
            pygame.transform.scale(
                self.render_surface,
                self.screen.get_size()),
            (0, 0)
        )

        pygame.event.pump()
        pygame.display.update()

    def close(self):
        if self.render_mode == 'human':
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            pygame.display.quit()
            pygame.quit()
