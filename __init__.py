from gymnasium.envs.registration import register
from TFTSolver.envs import TFTBoardEnv

register(
    id="TFT-Solver/tft_gym-v0",
    entry_point="tft_gym.envs:TFTBoardEnv",
    max_episode_steps=300,
)