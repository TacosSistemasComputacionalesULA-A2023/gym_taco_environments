import random
import time

import gym
from gym import spaces
import pygame

from . import settings


class Arm:
    def __init__(self, p=0, earn=0):
        self.probability = p
        self.earn = earn

    def execute(self):
        return self.earn if random.random() < self.probability else 0


class TwoArmedBanditEnv(gym.Env):
    def __init__(self):
        self.total_reward = 0
        self.delay = 0.5
        self.arms = (Arm(0.5, 1), Arm(0.1, 100))
        self.observation_space = spaces.Discrete(1)
        self.action_space = spaces.Discrete(len(self.arms))
        pygame.init()
        pygame.display.init()
        self.window = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOWS_HEIGHT))
        pygame.display.set_caption("Two-Armed Bandit Environment")
        self.action = None
        self.reward = None

    def _get_obs(self):
        return 0

    def _get_info(self):
        return {'state': 0}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if options is not None:
            if type(options) is not dict:
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get('delay', 0.5)

        observation = self._get_obs()
        info = self._get_info()
        return observation, info

    def step(self, action):
        self.action = action
        self.reward = self.arms[action].execute()
        observation = self._get_obs()
        info = self._get_info()

        self.render()
        time.sleep(self.delay)

        return observation, self.reward, False, False, info

    def render_main_elements(self):
        # Render total reward
        total_reward_font = settings.FONTS['large']
        total_reward_text_obj = total_reward_font.render(f"{self.total_reward}", True, (255, 255, 255))
        total_reward_text_rect = total_reward_text_obj.get_rect()
        total_reward_text_rect.center = (settings.WINDOW_WIDTH/2, settings.WINDOWS_HEIGHT/2)
        self.window.blit(total_reward_text_obj, total_reward_text_rect)

        # Render the first machine
        self.window.blit(settings.TEXTURES['machine'], (50, 100))

        # Render the second machine
        self.window.blit(
            settings.TEXTURES['machine'], (100 + settings.MACHINE_WIDTH, 100))

        x = 50 + settings.MACHINE_WIDTH / 2

        if self.action == 1:
            x += 50 + settings.MACHINE_WIDTH

        # Render the action
        arrow = settings.TEXTURES['arrow']
        w, h = arrow.get_size()
        self.window.blit(arrow, (x - w / 2 - 80, 150 +
                         settings.MACHINE_HEIGHT - h / 2))

    def _render_props(self):
        self.total_reward += self.reward
        self.window.fill((0, 0, 0))

        if self.reward is None or self.action is None:
            return

        x = 50 + settings.MACHINE_WIDTH / 2

        if self.action == 1:
            x += 50 + settings.MACHINE_WIDTH

        reward_font = settings.FONTS['large']
        text_obj = reward_font.render(f"{self.reward}", True, (255, 250, 26))
        text_rect = text_obj.get_rect()

        if self.reward != 0:
            self.render_main_elements()
            text_obj = reward_font.render(f"{self.reward}", True, (255, 250, 26))
            text_rect.center = (x, 80)
            self.window.blit(text_obj, text_rect)
            pygame.display.update()
            time.sleep(0.1)
            self.window.fill((0, 0, 0))
            self.render_main_elements()
            text_obj = reward_font.render(f"{self.reward}", True, (255, 255, 255))
            self.window.blit(text_obj, text_rect)
            pygame.display.update()
            
        # Render the reward 
        for n in range(15):
            self.window.fill((0, 0, 0))
            self.render_main_elements()
            text_rect.center = (x, 80 - n)
            self.window.blit(text_obj, text_rect)
            pygame.display.update()
        for n in range(15):
            self.window.fill((0, 0, 0))
            self.render_main_elements()
            text_rect.center = (x, 80 + n)
            self.window.blit(text_obj, text_rect)
            pygame.display.update()

    def render(self):
        self._render_props()

        pygame.event.pump()
        pygame.display.update()

    def close(self):
        pygame.display.quit()
        pygame.font.quit()
        pygame.quit()
