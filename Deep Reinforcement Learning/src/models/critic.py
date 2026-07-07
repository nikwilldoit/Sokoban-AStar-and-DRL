import torch
from torch import nn

class Critic(nn.Module):

    def __init__(self , cnn):
        super().__init__()

        self.cnn = cnn

        self.value = nn.Sequential(
            nn.Linear(cnn.output_features, 512),
            nn.ReLU(),

            nn.Linear(512, 256),
            nn.ReLU(),

            nn.Linear(256, 128),
            nn.ReLU(),

            nn.Linear(128, 1)
        )

    def forward(self,state):

        features = self.cnn(state)

        v_value = self.value(features)

        return v_value
    