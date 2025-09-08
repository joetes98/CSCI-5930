import gymnasium as gym
import math
import imageio.v2 as imageio
import os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from joblib import load, dump
import pandas as pd
from gymnasium.wrappers import RecordEpisodeStatistics, RecordVideo

#number of episodes
m = 100

#The CartPole-v0 environment with a random agent
# Goal is to control the cart (i.e., platform) with a pole attached by its bottom prt.
# Trick: The pole tends to fall right or left and you would need to balance it by moving the cart to the right or left on every step.
render_mode = 'rgb_array' #or, 'human'
env = gym.make("CartPole-v0", render_mode=render_mode)

# Video directory
try:
    os.mkdir("./video")
except:
    pass

# Add video recording for every episode
env = RecordVideo(
    env,
    video_folder="video",    # Folder to save videos
    name_prefix="deterministic",               # Prefix for video filenames
    episode_trigger=lambda x: True    # Record every episode
)

# Add episode statistics tracking
env = RecordEpisodeStatistics(env, buffer_length=m)

#Here below, we created the environment and initialized few variables.
total_reward = 0.0
total_steps = 0
observation, info = env.reset(seed=42)


episode = 1
for _ in tqdm(range(m)):
    step = 0
    terminated = False
    last = 1
    while not terminated:

        action = last
        observation, reward, terminated, truncated, info = env.step(action)
        step += 1
        total_reward += reward
        total_steps += 1
        last = 1 - last

        if terminated:
            episode += 1
            step = 0
            total_reward = 0
            observation, info = env.reset()
            #break

env.close()

# Metrics
max = np.max(env.return_queue)
mean = np.mean(env.return_queue)
std = np.std(env.return_queue)
print({f"Max Reward: {max}, Average Reward: {mean}, Standard Deviation: {std}"})