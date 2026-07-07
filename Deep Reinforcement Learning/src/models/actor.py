import torch
from torch import nn

class Actor(nn.Module):

    def __init__(self,num_actions, cnn):
        super().__init__()

        #shared neural network with critic
        self.cnn = cnn
    
        self.policy = nn.Sequential(
            nn.Linear(cnn.output_features, 512),
            nn.ReLU(),

            nn.Linear(512, 256),
            nn.ReLU(),

            nn.Linear(256, 128),
            nn.ReLU(),
            
            nn.Linear(128, num_actions)

        )

    def forward(self,state):
        features = self.cnn(state)

        logits = self.policy(features)

        return logits
        
    
    