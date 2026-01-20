from stable_baselines3 import PPO
from rl_env_flappy import FlappyEnv
import time

# Load enviorment
env = FlappyEnv()
obs, _ = env.reset()

# Loading model path
model_path = "models/PPO/RL_FLAP_1MIL" 
model = PPO.load(model_path, env=env, device="cuda")

# PLay Loop
while True:
    # This does the actions by prediction
    action, _states = model.predict(obs)
    
    # Do the action
    obs, rewards, terminated, truncated, info = env.step(action)
    
    # Draw it to the screen
    env.render()

    if terminated:
        obs, _ = env.reset()