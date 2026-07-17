from environment.levels import GameLevels
import utils.config as config
from environment.sokoban_env import SokobanEnv
import torch
from agent.memory import Memory
from agent.ppo_agent import PPOAgent

from utils.logger import Logger


class Trainer:

    def __init__(self):

        self.env = SokobanEnv()

        self.agent = PPOAgent()

        if config.LOAD_CHECKPOINT:
            self.agent.load(config.CHECKPOINT_PATH)

        self.memory = Memory()

        self.logger = Logger()

        self.total_steps = 0
        self.episode = 0

    def train(self):

        for episode in range(config.START_EPISODE, config.TOTAL_EPISODES):

            self.episode = episode

            self.train_episode()

            if self.episode % config.SAVE_EVERY == 0:

                self.agent.save(
                    f"checkpoints/ppo_{self.episode}.pt"
                )

            if self.episode % config.EVALUATE_EVERY == 0:

                self.evaluate()


    def train_episode(self):

        level_path = self.choose_level()
        self.env.set_level(level_path)
        observation, _ = self.env.reset()

        episode_reward = 0

        terminated = False
        truncated = False

        while not (terminated or truncated):

            #Select action from current policy
            action, log_prob, value = self.agent.select_action(observation)

            #Execute action
            next_observation, reward, terminated, truncated, info = self.env.step(action)

            done = terminated or truncated

            #Store transition
            self.memory.store(
                observation=torch.tensor(observation, dtype=torch.float32),
                action=action,
                reward=reward,
                done=done,
                log_prob=log_prob,
                value=value)

            #PPO update every rollout
            if self.memory.size() >= config.ROLLOUT_STEPS:

                self.agent.update(self.memory)

                self.memory.clear()

            observation = next_observation

            episode_reward += reward
            self.total_steps += 1

        #Log episode
        self.logger.log_episode(
            episode=self.episode,
            reward=episode_reward,
            steps=self.env.steps,
            completed=info["completed"],
            deadlock=info["deadlock"]
        )

    def evaluate(self):

        print("\n========== Evaluation ==========\n")

        for difficulty in GameLevels.DIFFICULTIES:

            levels = GameLevels.get_levels(difficulty)

            for level_path in levels:

                total_reward = 0.0
                total_steps = 0
                successes = 0
                deadlocks = 0

                for _ in range(config.EVALUATION_EPISODES):

                    self.env.set_level(level_path)

                    observation, _ = self.env.reset()

                    terminated = False
                    truncated = False

                    while not (terminated or truncated):

                        action = self.agent.predict(observation)

                        observation, reward, terminated, truncated, info = \
                            self.env.step(action)

                        total_reward += reward

                    total_steps += info["steps"]

                    if info["completed"]:
                        successes += 1

                    if info["deadlock"]:
                        deadlocks += 1

                self.logger.log_evaluation(
                    episode=self.episode,
                    level=f"{difficulty}/{level_path.name}",
                    success_rate=100 * successes / config.EVALUATION_EPISODES,
                    average_reward=total_reward / config.EVALUATION_EPISODES,
                    average_steps=total_steps / config.EVALUATION_EPISODES,
                    deadlocks=deadlocks
                )

        print("\n===============================\n")
        

    def choose_level(self):

        if config.USE_CURRICULUM:

            progress = self.episode / config.TOTAL_EPISODES

            if progress < 0.25:

                difficulties = [
                    "easy"
                ]

            elif progress < 0.50:

                difficulties = [
                    "easy",
                    "medium"
                ]

            elif progress < 0.75:

                difficulties = [
                    "easy",
                    "medium",
                    "hard"
                ]

            else:

                difficulties = [
                    "easy",
                    "medium",
                    "hard",
                    "expert"
                ]

        else:

            difficulties = [
                "easy"
            ]

            #"medium",
             #   "hard",
              #  "expert"
        return GameLevels.random_level(difficulties)