import torch


class Memory:

    def __init__(self):
        self.clear()


    def store(
        self,
        observation,
        action,
        reward,
        done,
        log_prob,
        value
    ):
        
        self.observations.append(observation)
        self.actions.append(action)
        self.rewards.append(reward)
        self.dones.append(done)
        self.log_probs.append(log_prob)
        self.values.append(value)


    def clear(self):

        self.observations = []
        self.actions = []
        self.rewards = []
        self.dones = []
        self.log_probs = []
        self.values = []


    def size(self):

        return len(self.actions)


    def get_tensors(self, device):

        observations = torch.tensor(
            self.observations,
            dtype=torch.float32,
            device=device
        )

        actions = torch.tensor(
            self.actions,
            dtype=torch.long,
            device=device
        )

        rewards = torch.tensor(
            self.rewards,
            dtype=torch.float32,
            device=device
        )

        dones = torch.tensor(
            self.dones,
            dtype=torch.float32,
            device=device
        )

        log_probs = torch.tensor(
            self.log_probs,
            dtype=torch.float32,
            device=device
        )

        values = torch.tensor(
            self.values,
            dtype=torch.float32,
            device=device
        )

        return (
            observations,
            actions,
            rewards,
            dones,
            log_probs,
            values
        )