import gymnasium as gym
import math
import imageio.v2 as imageio
import os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from joblib import load, dump
import pandas as pd

#number of episodes
m = 100



#The CartPole-v0 environment with a random agent
# Goal is to control the cart (i.e., platform) with a pole attached by its bottom prt.
# Trick: The pole tends to fall right or left and you would need to balance it by moving the cart to the right or left on every step.
render_mode = 'rgb_array' #or, 'human'
env = gym.make("CartPole-v0", render_mode=render_mode)
# Initialize empty buffer for the images that will be stiched to a gif
# Create a temp directory
filenames = []
try:
    os.mkdir("./temp")
except:
    pass

#Here below, we created the environment and initialized few variables.
total_reward = 0.0
total_steps = 0
observation, info = env.reset(seed=42)

df = pd.DataFrame(columns=["Episode", "Total Reward"])

episode = 1
for _ in tqdm(range(m)):
    step = 0
    terminated = False
    while not terminated:
        # Plot the previous state and save it as an image that 
        # will be later patched together sa a .gif
        img = plt.imshow(env.render())

        plt.title("Episode: {}, Step: {}".format(episode,step))
        plt.axis('off')
        plt.savefig("./temp/{}_{}.png".format(episode,step))
        plt.close()
        filenames.append("./temp/{}_{}.png".format(episode,step))

        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        step += 1
        total_reward += reward
        total_steps += 1

        if terminated:
            df.loc[_] = [episode, total_reward]
            episode += 1
            step = 0
            total_reward = 0
            observation, info = env.reset()
            #break

max = df['Total Reward'].max()
mean = df['Total Reward'].mean()
std = df['Total Reward'].std()
print(df)
print({f"Max Reward: {max}, Average Reward: {mean}, Standard Deviation: {std}"})

#print('Episode terminated in {} steps\nTotal rewards accumulated = {}'.format(total_steps,total_reward))
# Stitch the images together to produce a .gif
try:
    os.mkdir("./video")
except:
    pass

with imageio.get_writer('./video/CartPole-v0-random.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)

# Cleanup the images for the next run
for f in filenames:
    os.remove(f)


env.close()