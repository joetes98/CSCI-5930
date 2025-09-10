import gymnasium as gym
import math
import imageio.v2 as imageio
import os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from joblib import load, dump
import pandas as pd
from gymnasium.wrappers import RecordEpisodeStatistics, RecordVideo, TimeLimit
import random

#number of episodes
m = 100

render_mode = 'rgb_array'
env = gym.make("MountainCarContinuous-v0", render_mode = render_mode)

# Video directory
try:
    os.mkdir("./video")
except:
    pass

# Limit episodes to 200 steps
env = TimeLimit(env, max_episode_steps=200)

# Add video recording for every episode
env = RecordVideo(
    env,
    video_folder="video",    # Folder to save videos
    name_prefix="deterministicMountainCar",   # Prefix for video filenames
    episode_trigger=lambda x: x < m    # Record every episode
)

# Add episode statistics tracking
env = RecordEpisodeStatistics(env, buffer_length=m)

#Here below, we created the environment and initialized few variables.
total_reward = 0.0
total_steps = 0
observation, info = env.reset()

episode_rewards = []

episode = 1
for _ in tqdm(range(m)):
    observation, info = env.reset()
    total_reward = 0
    step = 0
    terminated = False
    truncated = False
    while not (terminated or truncated):

        if observation[1] < 0:
            action = [random.uniform(-1.0, 0.0)]
        elif observation[1] >= 0:
            action = [random.uniform(0.0, 1.0)]
        observation, reward, terminated, truncated, info = env.step(action)
        step += 1
        total_reward += reward
        total_steps += 1

        if terminated or truncated:
            # print(f"Episode {episode} ended at step {step}")
            # print(f"Terminated: {terminated}, Truncated: {truncated}")
            # print(f"Final position: {observation[0]}")
            # print(f"Total reward: {total_reward}")
            episode_rewards.append(total_reward)
            episode += 1
            step = 0

env.close()

# Metrics
max = np.max(env.return_queue)
mean = np.mean(env.return_queue)
std = np.std(env.return_queue)
print({f"Max Reward: {max}, Average Reward: {mean}, Standard Deviation: {std}"})