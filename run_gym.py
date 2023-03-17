import gymnasium as gym
import numpy as np
import tft_gym.tft_gym as tft_gym
import random as random
# env = gym.make("tft_gym/tft_gym-v0")
env = tft_gym.TFTBoardEnv()
observation, info = env.reset()

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
    # if random.random() <= ep:
    #     print(model.Q)
    #     return np.random.choice(model.Q)
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

for _ in range(1000):
    # 4 actions, 100 hp
    qlm = QLearningModel([0 for i in range(101)], [0 for i in range(4)], .9, .001)
    action = env.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)
    old_obs = observation
    iterations = 100
    for i in range(iterations):
        s = observation["hp"]
        s1 = old_obs["hp"]
        action = np.argmax(qlm.Q[s,:] + np.random.randn(1,4)*(1./(i+1)))
        observation, reward, terminated, truncated, info = env.step(action)
        qlm.Q[s, action] += qlm.lr * (reward + qlm.discount*np.max(qlm.Q[s1, :]) - qlm.Q[s,action])
        old_obs = observation
        print(reward)
        if terminated or truncated:
            policy = greedy_policy(qlm)
            print("Final policy:", policy)
            observation, info = env.reset()

env.close()
