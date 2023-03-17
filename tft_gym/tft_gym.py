import numpy as np
import math
import random
import pandas as pd


import gymnasium as gym
from gymnasium import spaces

class TFTBoardEnv(gym.Env):

    def __init__(self, render_mode=None, size=5):
        # self.size = size  # The size of the square grid
        # self.window_size = 512  # The size of the PyGame window
        
        # Observations are dictionaries with HP, gold, and player level
        self.observation_space = spaces.Dict(
            {
                "hp": spaces.Discrete(100),
                "gold": spaces.Discrete(200), # assume max gold is 200
                "level": spaces.Discrete(9),
                "your_units": spaces.Discrete(10),
                "enemy_units": spaces.Discrete(10),
                "n_states": spaces.Discrete(100 * 200 * 9 * 10 * 10),
            }
        )

        # We have 4 actions, corresponding to "reroll", "increase level", "open", "do nothing"
        self.action_space = spaces.Discrete(4)
    def _get_obs(self):
        return {"hp": self._hp, "level": self._level, "gold": self._gold, "units": self._your_units, "enemy_units": self._enemy_units}
    
    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self._hp = 100
        self._level = 1
        self._gold = 0
        self._your_units = 1
        self._enemy_units = 1

        observation = self._get_obs()
        return observation, None     
    
    def step(self, action):
        terminated = False
        gold_spent = 0
        if action == 0:
            if np.random.random() < .33: # we can change this for final version, assuming 1 guy in lobby high rolled
               self._hp -= 5
            gold_spent += 10
        if action == 1:
            gold_spent += 20
        if action == 2:
            self._gold += 10
            self._hp -= 10
        if action == 3:
            self._gold += 5
            if np.random.random() < .5:
                self._hp -= 5
        if (self._hp <= 0):
            terminated = True
        reward = (self._your_units - self._enemy_units * self._level) + self._gold - np.sqrt(gold_spent)
        self._gold -= gold_spent
        return self._get_obs(), reward, terminated, False, None #leaving info as none

# QLearning("data/small.csv", 100, 4, .95, .2, 'small', 1)