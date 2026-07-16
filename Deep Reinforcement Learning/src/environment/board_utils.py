from environment.actions import DIRECTIONS
from environment.tiles import Tile
class Board:

    @staticmethod
    def is_valid_move(row, col, board, direction):

        #Check board boundaries
        if row < 0 or row >= len(board):
            return False

        if col < 0 or col >= len(board[row]):
            return False

        target_cell = board[row][col]

        
        if target_cell == Tile.WALL:
            return False

        #Box or box on target
        if target_cell == Tile.BOX or target_cell == Tile.BOX_ON_TARGET:

            next_row = row + DIRECTIONS[direction][0]
            next_col = col + DIRECTIONS[direction][1]



            #Check board boundaries
            if next_row < 0 or next_row >= len(board):
                return False

            if next_col < 0 or next_col >= len(board[next_row]):
                return False

            after_box = board[next_row][next_col]

            #Box cannot be pushed into wall or another box
            return after_box not in (Tile.WALL, Tile.BOX, Tile.BOX_ON_TARGET)

        #Empty space or target
        return True


    @staticmethod
    def move_player(newRow, newCol, grid, direction):

        moved = False
        pushed_box = False
        box_on_target = False
        box_left_target = False

        oldRow = newRow - DIRECTIONS[direction][0]
        oldCol = newCol - DIRECTIONS[direction][1]

        #checking limits
        if oldRow < 0 or oldRow >=  len(grid) or oldCol < 0 or oldCol >= len(grid[0]):
            return grid

        oldTile = grid[oldRow][oldCol]
        targetTile = grid[newRow][newCol]

        
        #calculating what the player leaves behind
        if oldTile == Tile.PLAYER_ON_TARGET:
            grid[oldRow][oldCol] = Tile.TARGET
        else:
            grid[oldRow][oldCol] = Tile.EMPTY


        if targetTile == Tile.EMPTY or targetTile == Tile.TARGET:
            
            moved = True

            if targetTile == Tile.TARGET:
                grid[newRow][newCol] = Tile.PLAYER_ON_TARGET
            else:
                grid[newRow][newCol] = Tile.PLAYER
            
            return grid, moved, pushed_box, box_on_target, box_left_target

        if targetTile == Tile.BOX or targetTile == Tile.BOX_ON_TARGET:
            boxNewRow = newRow + DIRECTIONS[direction][0]
            boxNewCol = newCol + DIRECTIONS[direction][1]

            if boxNewRow < 0 or boxNewRow >= len(grid) or boxNewCol < 0 or boxNewCol >= len(grid[0]):
                return grid, moved, pushed_box, box_on_target, box_left_target
        
            afterBoxTile = grid[boxNewRow][boxNewCol]


            #check if space exist for the box to be moved
            if afterBoxTile == Tile.EMPTY or afterBoxTile == Tile.TARGET:
                moved = True
                pushed_box = True
                
                #moved the box
                if afterBoxTile == Tile.TARGET:
                    grid[boxNewRow][boxNewCol] = Tile.BOX_ON_TARGET
                    box_on_target = True
                else:
                    grid[boxNewRow][boxNewCol] = Tile.BOX
                

                #player moves in the position of the box
                if targetTile == Tile.BOX_ON_TARGET:
                    box_left_target = True
                    grid[newRow][newCol] = Tile.PLAYER_ON_TARGET
                else:
                    grid[newRow][newCol] = Tile.PLAYER

                return grid, moved, pushed_box, box_on_target, box_left_target
            
        if oldTile == Tile.PLAYER_ON_TARGET:
            grid[oldRow][oldCol] = Tile.PLAYER_ON_TARGET
        else:
            grid[oldRow][oldCol] = Tile.PLAYER

        return grid, moved, pushed_box, box_on_target, box_left_target


                
    @staticmethod
    def find_player(grid):
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                
                if grid[r][c] == Tile.PLAYER or grid[r][c] == Tile.PLAYER_ON_TARGET:
                    return (r, c)

            
        return (-1, -1)


    @staticmethod
    def copy_grid(grid):

        newGrid = [row.copy() for row in grid]
        return newGrid


    @staticmethod
    def pad_board(grid):

        rows = len(grid)
        cols = 0

        #Find the longest row
        for row in grid:
            cols = max(cols, len(row))

        #Create a new board filled with walls
        new_board = [[Tile.WALL for _ in range(cols + 2)] for _ in range(rows + 2)]

        #Copy the original board
        for i in range(rows):
            for j in range(len(grid[i])):
                new_board[i + 1][j + 1] = grid[i][j]

        return new_board


    @staticmethod
    def is_completed(board):

        for row in board:
            for cell in row:

                #Free box or free target still exists
                if cell in (Tile.BOX, Tile.TARGET):
                    return False

        return True


        