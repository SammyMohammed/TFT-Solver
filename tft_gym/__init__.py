from gymnasium.envs.registration import register

register(
    id="tft_gym/tft_gym-v0",
    entry_point="tft_gym.envs:TFTBoardEnv",
    max_episode_steps=300,
)