from environment.tiles import Tile

class DeadlockDetector:

    #check if a move causes deadlock
    @staticmethod
    def isDeadlock(board):

        for row in range(len(board)):
            for col in range(len(board[0])):

                if row <= 0 or row >= len(board) - 1 or col <= 0 or col >= len(board[0]) - 1:
                    continue

                if board[row][col] != Tile.BOX:
                    continue
                if board[row][col] == Tile.BOX_ON_TARGET:
                    continue

                if board[row][col] == Tile.BOX:

                    #Corridor deadlock check
                    if DeadlockDetector._is_corridor_deadlock(board, row, col):
                        return True

                    wallDirections = DeadlockDetector._check_four_directions(board, row, col)

                    if len(wallDirections) == 0:
                        continue

                    elif len(wallDirections) == 2:
                        if DeadlockDetector._is_corner_deadlock(board, row, col) and board[row][col] != Tile.TARGET:
                            return True

                    elif len(wallDirections) > 2:
                        return True

                    else:
                        coordinates = wallDirections[0]
                        identifier = coordinates[0]
                        targetExistsUp = False
                        targetExistsdown = False

                        if identifier == 1:  #column case
                            UpBlocked = False
                            downBlocked = False

                            #scan row to left
                            for k in range(col, -1, -1):
                                if board[row][k] == Tile.WALL:
                                    UpBlocked = True
                                    break
                                if board[row][k] == Tile.TARGET:
                                    targetExistsUp = True
                                    break

                        #scan row to right
                            for k in range(col, len(board[0])):
                                if board[row][k] == Tile.WALL:
                                    downBlocked = True
                                    break
                                if board[row][k] == Tile.TARGET:
                                    targetExistsdown = True
                                    break

                            fullWalls = True
                            for k in range(len(board[0])):
                                if board[row][k] != Tile.WALL:
                                    fullWalls = False
                                    break

                            if (not targetExistsUp and
                                    not targetExistsdown and
                                    downBlocked and
                                    UpBlocked):
                                if fullWalls:
                                    return True

                        elif identifier == 0:  #row case
                            leftBlocked = False
                            rightBlocked = False
                            targetExistsleft = False
                            targetExistsright = False

                            #scan column up
                            for k in range(row, -1, -1):
                                if board[k][col] == Tile.WALL:
                                    leftBlocked = True
                                    break
                                if board[k][col] == Tile.TARGET:
                                    targetExistsleft = True
                                    break

                            fullWalls = True
                            for chars in board:
                                if chars[col] != Tile.WALL:
                                    fullWalls = False
                                    break

                            #scan column down
                            for k in range(row, len(board)):
                                if board[k][col] == Tile.WALL:
                                    rightBlocked = True
                                    break
                                if board[k][col] == Tile.TARGET:
                                    targetExistsright = True
                                    break

                            if (not targetExistsright and
                                rightBlocked and
                                not targetExistsleft and
                                leftBlocked):
                                if fullWalls:
                                    return True

        return False



    @staticmethod
    def _is_corridor_deadlock(board, row, col):
        rows = len(board)
        cols = len(board[0])

        horizontal = (col - 1 >= 0 and
                      col + 1 < cols and
                      board[row][col - 1] == Tile.WALL and
                      board[row][col + 1] == Tile.WALL)
        

        vertical = (row - 1 >= 0 and
                    row + 1 < rows and
                    board[row - 1][col] == Tile.WALL and
                    board[row + 1][col] == Tile.WALL)


        if (not horizontal and not vertical): 
            return False

        holes = 0

        if vertical:
            
            #Check for box or goal in this tunnel
            boxExists = False
            goalExists = False

            for value in board:
                if value[col] == Tile.BOX:
                    boxExists = True
                
                if value[col] == Tile.TARGET:
                    goalExists = True


            #check left and right
            for chars in board:
                if col - 1 >= 0 and col + 1 < cols:
                    if chars[col - 1] != Tile.WALL or chars[col + 1] != Tile.WALL:
                        holes = holes + 1
                    
                
            
            return holes == 0  and not boxExists  and not goalExists
        
        if horizontal:

            #check for box or goal in this tunnel
            boxExists = False
            goalExists = False

            for m in range(cols):

                if board[row][m] == Tile.BOX:
                    boxExists = True
                
                if board[row][m] == Tile.TARGET:
                    goalExists = True
                
            
            #check up and down
            for c in range(cols):
                if row - 1 >= 0 and row + 1 < rows:
                    if board[row - 1][c] != Tile.WALL or board[row + 1][c] != Tile.WALL:
                        holes = holes + 1
                    
                
            
            return holes == 0 and  not boxExists and not goalExists
    



    @staticmethod
    def _is_corner_deadlock(board, row, col):
        rows = len(board)
        cols = len(board[0])
        isCorner = False

        #check boundaries before each access
        if row - 1 >= 0 and col - 1 >= 0 and board[row - 1][col] == Tile.WALL and board[row][col - 1] == Tile.WALL:
            isCorner = True
        elif row - 1 >= 0 and col + 1 < cols and board[row - 1][col] == Tile.WALL and board[row][col + 1] == Tile.WALL:
            isCorner = True
        elif row + 1 < rows and col - 1 >= 0 and board[row + 1][col] == Tile.WALL and board[row][col - 1] == Tile.WALL:
            isCorner = True
        elif row + 1 < rows and col + 1 < cols and board[row + 1][col] == Tile.WALL and board[row][col + 1] == Tile.WALL:
            isCorner = True
        
        return isCorner



    @staticmethod
    def _check_four_directions(board, row, col):

        wallDirections = []

        rows = len(board)
        cols = len(board[0])

        #up
        if row - 1 >= 0 and board[row - 1][col] == Tile.WALL:
            wallDirections.append([1])

        #down
        if row + 1 < rows and board[row + 1][col] == Tile.WALL:
            wallDirections.append([1])

        #left
        if col - 1 >= 0 and board[row][col - 1] == Tile.WALL:
            wallDirections.append([0])

        #right
        if col + 1 < cols and board[row][col + 1] == Tile.WALL:
            wallDirections.append([0])

        return wallDirections