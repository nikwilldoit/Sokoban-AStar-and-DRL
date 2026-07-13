import numpy as np
from gymnasium import spaces
from environment.tiles import Tile

class ObservationEncoder:

    SYMBOL_TO_CHANNEL = {
        Tile.EMPTY: 0,  #Empty space
        Tile.PLAYER: 1,   #Player
        Tile.BOX: 2,   #Box
        Tile.WALL: 3,   #Wall
        Tile.TARGET: 4,   #Target
        Tile.BOX_ON_TARGET: 5,   #Box on Target
        Tile.PLAYER_ON_TARGET: 6    #Player on Target
    }

    @staticmethod
    def encode(board):

        height = len(board)
        width = len(board[0])

        observation = np.zeros((7, height, width), dtype=np.float32)

        for row in range(height):
            for col in range(width):
                
                symbol = board[row][col]

                if symbol in ObservationEncoder.SYMBOL_TO_CHANNEL:
                    channel = ObservationEncoder.SYMBOL_TO_CHANNEL[symbol]
                    observation[channel, row, col] = 1.0

        return observation


    @staticmethod
    def observation_space(height, width):

        return spaces.Box(
            low=0.0,
            high=1.0,
            shape=(7, height, width),
            dtype=np.float32
        )
