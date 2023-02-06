import time

import numpy as np

import gym
from gym import spaces
import pygame

from . import settings
from .world import World
import json
from .utils import utils

class RobotBatteryEnv(gym.Env):
    metadata = {"render_modes": ["human", "ansi"], "render_fps": 4}

    def __init__(self, **kwargs):
        super().__init__()

        generator = utils.SpaceGenerator(seed=settings.SEED)
        self.initial_battery = 16
        self.current_battery = 16
        self.render_mode = kwargs['render_mode']
        self.observation_space = spaces.Discrete(settings.NUM_TILES)
        self.action_space = spaces.Discrete(settings.NUM_ACTIONS)
        self.current_action = 1
        self.current_state = 0
        self.current_reward = 0.0
        self.delay = kwargs['delay']
        self.P = generator.generate_robot_battery_pmatrix(settings.COLS)
        settings.P = self.P
        self.world = World(
            "Robot Battery Environment",
            self.current_state,
            self.current_action,
            self.render_mode
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get('delay', 0.5)

        np.random.seed(seed)
        self.current_state = 0
        self.current_action = 1
        self.world.reset(self.current_state, self.current_action)
        return 0, {}

    def step(self, action):
        self.current_action = action
        if (self.current_battery > 0):
            self.current_battery -= 1
        
        print(f'self.current_battery {self.current_battery}')

        possibilities = self.P[self.current_state][self.current_action]

        if np.random.random() < 1 - self.current_battery / self.initial_battery:
            possibilities = self.P[self.current_state][np.random.randint(0, 4)]

        p = 0
        i = 0

        r = np.random.random()
        terminated = False
        while r > p:
            r -= p
            p, self.current_state, self.current_reward, terminated = possibilities[i]
            i += 1

        self.world.update(
            self.current_state,
            self.current_action,
            self.current_reward,
            terminated
        )

        self.render()
        time.sleep(self.delay)

        return self.current_state, self.current_reward, terminated, False, {}

    def render(self):
        self.world.render(self.render_mode)

    def close(self):
        self.world.close()
