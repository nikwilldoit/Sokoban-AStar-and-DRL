import torch
from torch import nn

class CNN(nn.Module):
    def __init__(self):
        super().__init__()

        #pooling. Maybe 8 or 4. Depends on Height and Width of the Game
        self.pool_size = 6
        
        self.features = nn.Sequential(

            #Input channels:
            #Player, Box, Wall, Target, Box on Target, Player on Target
            nn.Conv2d(7, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),

            nn.AdaptiveAvgPool2d((self.pool_size,self.pool_size))
        )

        self.flatten = nn.Flatten()

        self.output_features = 128 * self.pool_size * self.pool_size

    
    def forward(self,x):
        x = self.features(x)
        x = self.flatten(x)
        return x