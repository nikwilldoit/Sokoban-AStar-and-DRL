import csv
import os


class Logger:

    def __init__(self, log_dir="logs"):

        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

        self.csv_file = os.path.join(log_dir, "training_log.csv")

        #Create csv file
        if not os.path.exists(self.csv_file):

            with open(self.csv_file, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Episode",
                    "Reward",
                    "Steps",
                    "Completed",
                    "Deadlock"
                ])


    def log_episode(
        self,
        episode,
        reward,
        steps,
        completed,
        deadlock
    ):

        print(
            f"Episode {episode:5d} | "
            f"Reward: {reward:8.2f} | "
            f"Steps: {steps:4d} | "
            f"Completed: {completed} | "
            f"Deadlock: {deadlock}"
        )

        with open(self.csv_file, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                episode,
                reward,
                steps,
                completed,
                deadlock
            ])


    def log_model(self, path):

        print(f"Model saved to {path}")


    def log_evaluation(
        self,
        reward,
        completed
    ):

        print("\n========== Evaluation ==========")
        print(f"Reward: {reward:.2f}")
        print(f"Completed: {completed}")
        print("================================\n")