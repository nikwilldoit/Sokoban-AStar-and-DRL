import torch
import torch.nn as nn
from torch.distributions import Categorical
from models.actor_critic import ActorCritic
import utils.config as config
import os

class PPOAgent:

    def __init__(self):
        
        self.device = config.DEVICE

        self.policy = ActorCritic().to(self.device)

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

        
        logits, value = self.policy(observation)

        distribution = Categorical(logits=logits)

        action = distribution.sample()

        log_prob = distribution.log_prob(action)

        return (
            action.item(),
            log_prob.detach(),
            value.squeeze().detach()
        )
    


    #Used during PPO update.
    def evaluate_actions(self, observations, actions):

        logits, values = self.policy(observations)

        distribution = Categorical(logits=logits)

        log_prob = distribution.log_prob(actions)

        entropy = distribution.entropy()

        return log_prob, values.squeeze(), entropy
    

    def save(self, path):

        directory = os.path.dirname(path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        torch.save(
            self.policy.state_dict(),
            path
        )

    def load(self, path):

        self.policy.load_state_dict(
            torch.load(
                path
            )
        )

        self.policy.eval()


    def update(self, memory):

        observations = torch.stack(memory.observations).to(config.DEVICE)

        actions = torch.tensor(
            memory.actions,
            dtype=torch.long,
            device=config.DEVICE
        )

        rewards = torch.tensor(
            memory.rewards,
            dtype=torch.float32,
            device=config.DEVICE
        )

        dones = torch.tensor(
            memory.dones,
            dtype=torch.float32,
            device=config.DEVICE
        )

        old_log_probs = torch.stack(memory.log_probs).detach().to(config.DEVICE)

        values = torch.stack(memory.values).squeeze().detach().to(config.DEVICE)


    
        #Compute Advantages (GAE)

        advantages = torch.zeros_like(rewards)

        returns = torch.zeros_like(rewards)

        gae = 0.0

        next_value = 0.0


        for t in reversed(range(len(rewards))):

            mask = 1.0 - dones[t]

            delta = (
                rewards[t]
                + config.GAMMA * next_value * mask
                - values[t]
            )

            gae = (
                delta
                + config.GAMMA
                * config.GAE_LAMBDA
                * mask
                * gae
            )

            advantages[t] = gae

            returns[t] = advantages[t] + values[t]

            next_value = values[t]

    #Normalize Advantages

        advantages = (
            advantages - advantages.mean()) / (advantages.std() + 1e-8)
        

        #PPO Optimizations

        dataset_size = len(rewards)

        for _ in range(config.UPDATE_EPOCHS):
            permutation = torch.randperm(dataset_size)

            for start in range(0,dataset_size,config.MINI_BATCH_SIZE):

                end = start + config.MINI_BATCH_SIZE

                batch = permutation[start:end]

                batch_obs = observations[batch]

                batch_actions = actions[batch]

                batch_old_log_probs = old_log_probs[batch]

                batch_returns = returns[batch]

                batch_advantages = advantages[batch]

            #Current Policy
      

                new_log_probs, state_values, entropy = \
                    self.evaluate_actions(
                        batch_obs,
                        batch_actions
                    )
            #PPO Ratio
        
                ratio = torch.exp(
                    new_log_probs -
                    batch_old_log_probs
                )   

            #Actor Loss
    
                surrogate1 = ratio * batch_advantages

                surrogate2 = torch.clamp(
                    ratio,
                    1.0 - config.CLIP_EPSILON,
                    1.0 + config.CLIP_EPSILON
                ) * batch_advantages

                actor_loss = -torch.min(
                    surrogate1,
                    surrogate2
                ).mean()

            #Critic Loss
                critic_loss = nn.functional.mse_loss(
                    state_values,
                    batch_returns
                )

            #Entropy

                entropy_loss = entropy.mean()

            
            #Total Loss
           
                loss = (
                    actor_loss
                    + config.VALUE_LOSS_COEF * critic_loss
                    - config.ENTROPY_COEF * entropy_loss
                )

            # Backpropagation
        
                self.optimizer.zero_grad()

                loss.backward()

                torch.nn.utils.clip_grad_norm_(
                    self.policy.parameters(),
                    config.MAX_GRAD_NORM
                )

                self.optimizer.step()


    @torch.no_grad()
    def predict(self, observation):

        if not torch.is_tensor(observation):

            observation = torch.tensor(
                observation,
                dtype=torch.float32,
                device=self.device
            )

        observation = observation.unsqueeze(0)

        logits, _ = self.policy(observation)

        action = torch.argmax(
            logits,
            dim=1
        )

        return action.item()
