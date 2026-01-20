import os
import torch
from stable_baselines3 import PPO
from rl_env_flappy import FlappyEnv

models_dir = "models/PPO" # Directory for storing models
log_dir = "logs" # Directory for storeing logs
model_name = "/addacustomnamebro" # Name it based on Timestep makes it easier to rem.
# Create these if not made
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)    

env = FlappyEnv()
env.reset()

model = PPO('MlpPolicy', env, verbose = 1, tensorboard_log = log_dir,device="cuda") #verbose true or 1 is logs, mlpPolicy is multi layer perceptron other wouldve been vision based but we dont need it.

# Total 1 million fps | approx 11 days something crazyyy right if delta time set to 0.016 under game.update()

TIMSTEPS = 1000000 
model.learn(total_timesteps= TIMSTEPS, reset_num_timesteps=False)

model.save(f"{models_dir}{model_name}")

obs, _ = env.reset()
