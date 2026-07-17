import os
import time



#when done, pygame is going to be implemented here
class Renderer:

    #Print the current Sokoban board.
    @staticmethod
    def render(board):

        print()

        for row in board:
            print("".join(row))



        print()

    @staticmethod
    def close():
        return