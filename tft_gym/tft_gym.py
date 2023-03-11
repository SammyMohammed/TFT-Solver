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
            gold_spent -= 10
        if action == 1:
            gold_spent -= 20
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
        return self._get_obs, reward, terminated, False, None #leaving info as none

class QLearningModel():
    def __init__(self, states, actions, discount, lr):
        self.states = states
        self.actions = actions
        self.discount = discount
        self.Q = np.zeros((len(states), len(actions)))
        self.lr = lr

def update_step(model, s, a, r, s1):
    model.Q[s, a] += model.lr * (r + model.discount*np.max(model.Q[s1, :]) - model.Q[s,a])
    return model

def greedy_policy(model, ep=.1):
    # add the epsilon part of greedy epsilon
    if random.random() <= ep:
        return np.random.choice(model.Q, axis=-1)
    return np.argmax(model.Q, axis=-1)

def QLearning(file, nstates, nactions, discount, lr, output, iterations):
    qlm = QLearningModel([0 for i in range(nstates)], [0 for i in range(nactions)], discount, lr)
    df = pd.read_csv(file)
    policy = None
    s2 = 0
    r2 = 0
    a2 = 0
    for i in range(iterations):
        for index, row in df.iterrows():
            s,a,r,sp = row
            s -= 1
            sp -= 1 
            a -= 1
            if s != s2:
                qlm = update_step(qlm, s2, a2, r2, s)
            s2 = s
            a2 = a
            r2 = r
    policy = greedy_policy(qlm)
    policy = policy + np.ones_like(policy)
    print("sheesh")
    policy.tofile(output + '.policy', sep="\n")
    print(output)

# QLearning("data/small.csv", 100, 4, .95, .2, 'small', 1)