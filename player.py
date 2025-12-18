import pygame
from settings import TILE, MAP_WIDTH, MAP_HEIGHT, BLUE

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE, TILE)
        self.anim = 0

    def move(self, dx, dy, dungeon):
        nx = self.rect.x + dx
        ny = self.rect.y + dy

        tx = nx // TILE
        ty = ny // TILE

        # stay inside map bounds AND walkable tiles
        if 0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT:
            if dungeon.is_walkable(tx, ty):
                self.rect.x = nx
                self.rect.y = ny

    def update(self):
        self.anim = (self.anim + 1) % 30

    def draw(self, screen):
        color = BLUE if self.anim < 15 else (90, 170, 255)
        pygame.draw.rect(screen, color, self.rect)
