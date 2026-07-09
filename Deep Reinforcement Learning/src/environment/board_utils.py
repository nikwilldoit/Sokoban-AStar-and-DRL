from environment.constants import DIRECTIONS

class Board:

    def is_valid_move(row, col, board, direction):

        #Check board boundaries
        if row < 0 or row >= len(board):
            return False

        if col < 0 or col >= len(board[row]):
            return False

        target_cell = board[row][col]

        #Wall
        if target_cell == '#':
            return False

        #Box or box on target
        if target_cell == '0' or target_cell == '*':

            next_row = row + DIRECTIONS[direction][0]
            next_col = col + DIRECTIONS[direction][1]

            #Check board boundaries
            if next_row < 0 or next_row >= len(board):
                return False

            if next_col < 0 or next_col >= len(board[next_row]):
                return False

            after_box = board[next_row][next_col]

            #Box cannot be pushed into wall or another box
            return after_box not in ('#', '0', '*')

        #Empty space or target
        return True





    def updateGrid():




    def findPlayer():



    def copyGrid():




    def makeRectangularWithBorder():



    def is_completed():


        