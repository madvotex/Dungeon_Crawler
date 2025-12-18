import pygame
from settings import WHITE

class UI:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 24)

    def text(self, screen, msg, x, y):
        screen.blit(self.font.render(msg, True, WHITE), (x, y))

    def compass(self, screen, x, y):
        self.text(screen, "N ↑", x, y)
        self.text(screen, "S ↓", x, y + 20)
        self.text(screen, "E →", x, y + 40)
        self.text(screen, "W ←", x, y + 60)
        self.text(screen, "Minimap", x, y + 100)
