import pygame
from settings import *

class Door:
    def __init__(self):
        self.rect = pygame.Rect(720, 500, 40, 60)

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)


class Portal:
    def __init__(self):
        self.rect = pygame.Rect(350, 0, 80, 40)

    def draw(self, screen):
        pygame.draw.rect(screen, PURPLE, self.rect)


class Key:
    def __init__(self):
        self.rect = pygame.Rect(0,0,15,15)
        self.visible = False

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, YELLOW, self.rect)


class Pillar:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)