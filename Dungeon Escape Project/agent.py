import pygame
from settings import *

class Agent:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.alive = True
        self.has_key = False

    def step(self, action, pillars):
        if not self.alive:
            return

        dx, dy = 0, 0

        if action == 1: dy = -3
        elif action == 2: dy = 3
        elif action == 3: dx = -3
        elif action == 4: dx = 3

        # apply movement
        self.rect.x += dx
        self.rect.y += dy

        # boundary
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        # collision with pillars
        for p in pillars:
            if self.rect.colliderect(p.rect):
                self.rect.x -= dx
                self.rect.y -= dy

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, GREEN, self.rect)