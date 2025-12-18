import pygame
import random
from settings import TILE, RED

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE, TILE)
        self.alert_counter = 0
        self.vision_radius = 6     # tiles
        self.move_cooldown = 0     # slows enemy movement

    def can_see_player(self, dungeon, player):
        ex = self.rect.x // TILE
        ey = self.rect.y // TILE
        px = player.rect.x // TILE
        py = player.rect.y // TILE

        # distance check
        if abs(ex - px) > self.vision_radius or abs(ey - py) > self.vision_radius:
            return False

        # Bresenham line-of-sight (blocked by walls)
        dx = abs(px - ex)
        dy = abs(py - ey)
        sx = 1 if ex < px else -1
        sy = 1 if ey < py else -1
        err = dx - dy

        x, y = ex, ey
        while (x, y) != (px, py):
            if dungeon.map[y][x] == 0:  # WALL
                return False
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

        return True

    def update(self, dungeon, player):
        # slow movement: enemy moves once every 3 frames
        self.move_cooldown = (self.move_cooldown + 1) % 3
        if self.move_cooldown != 0:
            return

        if self.can_see_player(dungeon, player):
            self.alert_counter += 1
        else:
            self.alert_counter = 0

        dx = dy = 0

        if self.alert_counter >= 2:
            # chase player (slowly)
            if player.rect.x > self.rect.x:
                dx = 1
            elif player.rect.x < self.rect.x:
                dx = -1

            if player.rect.y > self.rect.y:
                dy = 1
            elif player.rect.y < self.rect.y:
                dy = -1
        else:
            # idle wandering
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])

        nx = self.rect.x + dx
        ny = self.rect.y + dy

        if dungeon.is_walkable(nx // TILE, ny // TILE):
            self.rect.x = nx
            self.rect.y = ny

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
