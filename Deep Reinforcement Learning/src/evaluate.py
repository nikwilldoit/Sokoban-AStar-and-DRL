from agent.trainer import Trainer


def main():

    trainer = Trainer()

    trainer.agent.load("checkpoints/ppo_2000.pt")

    trainer.evaluate()


if __name__ == "__main__":
    main()