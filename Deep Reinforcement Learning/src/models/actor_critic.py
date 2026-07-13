import torch
import torch.nn as nn
from models.cnn import CNN
from environment.actions import NUM_ACTIONS

class ActorCritic(nn.Module):

    def __init__(self):
        super().__init__()

        self.cnn = CNN()

        self.actor = nn.Sequential(
            nn.Linear(self.cnn.output_features,512),
            nn.ReLU(),
            nn.Linear(512,256),
            nn.ReLU(),
            nn.Linear(256, NUM_ACTIONS)
        )

        self.critic = nn.Sequential(
            nn.Linear(self.cnn.output_features,512),
            nn.ReLU(),
            nn.Linear(512,256),
            nn.ReLU(),
            nn.Linear(256,1)
        )


    def forward(self,state):

        features = self.cnn(state)

        logits = self.actor(features)
        value = self.critic(features)

        return logits,value
