
from environment.sokoban_env import SokobanEnv


if __name__ == "__main__":

    env = SokobanEnv(level_id=0)

    observation, info = env.reset()

    terminated = False
    truncated = False

    total_reward = 0
    step_count = 0

    while not (terminated or truncated):

        action = env.action_space.sample()

        observation, reward, terminated, truncated, info = env.step(action)

        total_reward += reward
        step_count += 1

        env.render()

    print(f"Steps: {step_count}")
    print(f"Total Reward: {total_reward}")

    env.close()