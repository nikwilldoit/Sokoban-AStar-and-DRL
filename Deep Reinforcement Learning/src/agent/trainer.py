import utils.config as config

from environment.sokoban_env import SokobanEnv

from agent.memory import Memory
from agent.ppo_agent import PPOAgent

from utils.logger import Logger


class Trainer:

    def __init__(self):

        self.env = SokobanEnv()

        self.agent = PPOAgent()

        self.memory = Memory()

        self.logger = Logger()

        self.total_steps = 0
        self.episode = 0

    def train(self):

        while self.episode < config.TOTAL_EPISODES:

            self.train_episode()

            self.episode += 1

            if self.episode % config.SAVE_EVERY == 0:

                self.agent.save(
                    f"checkpoints/ppo_{self.episode}.pt"
                )

            if self.episode % config.EVALUATE_EVERY == 0:

                self.evaluate()


    def train_episode():
        