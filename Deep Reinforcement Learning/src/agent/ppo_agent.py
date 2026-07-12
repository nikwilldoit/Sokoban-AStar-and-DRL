import torch
import torch.nn.functional as F
from torch.distributions import Categorical
from models.actor_critic import ActorCritic
import utils.config as config

class PPOAgent:

    def __init__(self):
        
        self.device = config.DEVICE

        self.policy = ActorCritic(config.NUM_ACTIONS).to(self.device)

        self.optimizer = torch.optim.Adam(
            self.policy.parameters(),
            lr=config.LEARNING_RATE
        )


    #Used during interaction with the environment.
    def select_action(self, observation):

        if not torch.is_tensor(observation):
            observation = torch.tensor(
                observation,
                dtype=torch.float32,
                device=self.device
            )

        observation = observation.unsqueeze(0)

        with torch.no_grad():
            logits, value = self.policy(observation)

            distribution = Categorical(logits=logits)

            action = distribution.sample()

            log_prob = distribution.log_prob(action)

        return (
            action.item(),
            log_prob.item(),
            value.squeeze().item()
        )
    
    #Used during PPO update.
    def evaluate_actions(self, observations, actions):

        logits, values = self.policy(observations)

        distribution = Categorical(logits=logits)

        log_prob = distribution.log_prob(actions)

        entropy = distribution.entropy()

        return log_prob, values.squeeze(-1), entropy
    

    def save(self, path):

        torch.save(
            self.policy.state_dict(),
            path
        )

    def load(self, path):

        self.policy.load_state_dict(
            torch.load(
                path, map_location=self.device
            )
        )

        self.policy.eval()
