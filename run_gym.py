import gymnasium as gym
import tft_gym.tft_gym as tft_gym
# env = gym.make("tft_gym/tft_gym-v0")
env = tft_gym.TFTBoardEnv()
observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)
    print(reward)
    if terminated or truncated:
        observation, info = env.reset()

env.close()
