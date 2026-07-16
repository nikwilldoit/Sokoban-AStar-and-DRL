import pygame
from environment.tiles import Tile

TILE_SIZE = 64

class Renderer:

    def __init__(self):

        pygame.init()

        self.images = {
            Tile.EMPTY: pygame.image.load("assets/floor.png"),
            Tile.WALL: pygame.image.load("assets/wall.png"),
            Tile.PLAYER: pygame.image.load("assets/player.png"), #THA DW PWS THA KATSW NA SETARW TO ANIMATION
                                                                 #GT DEN ELEGXETAI ME MOVEMENT
            Tile.BOX: pygame.image.load("assets/box.png"),
            Tile.TARGET: pygame.image.load("assets/target.png"),
            Tile.BOX_ON_TARGET: pygame.image.load("assets/box_target.png"),
            Tile.PLAYER_ON_TARGET: pygame.image.load("assets/player_target.png"),
        }

        for key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key],(TILE_SIZE, TILE_SIZE))

        self.screen = None

    def render(self, board):

        rows = len(board)
        cols = len(board[0])

        if self.screen is None:
            self.screen = pygame.display.set_mode((cols * TILE_SIZE, rows * TILE_SIZE))
            pygame.display.set_caption("Sokoban")

        self.screen.fill((0,0,0))

        for r in range(rows):
            for c in range(cols):

                tile = board[r][c]

                self.screen.blit(
                    self.images[tile],
                    (c*TILE_SIZE, r*TILE_SIZE)
                )

        pygame.display.flip()

    def close(self):
        pygame.quit()