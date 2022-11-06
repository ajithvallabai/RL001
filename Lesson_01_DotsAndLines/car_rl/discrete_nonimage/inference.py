import gym
from stable_baselines3 import PPO
from carenv import CarEnv

models_dir = "models/aaaaa_best_trained"

env = CarEnv()
env.reset()

model_path = f"{models_dir}/20000.zip"
model = PPO.load(model_path, env=env)

episodes = 500

for ep in range(episodes):
    obs = env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        print(rewards)