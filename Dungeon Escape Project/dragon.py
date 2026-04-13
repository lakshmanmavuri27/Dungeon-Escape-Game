import pygame
from settings import *

class Dragon:
    def __init__(self):
        self.rect = pygame.Rect(300, 200, 30, 30)
        self.alive = True
        self.speed = 1   # slower than agents

    def move(self, pillars, portal):
        if not self.alive:
            return

        # 🎯 move towards portal
        dx = 0
        dy = 0

        if portal.rect.x > self.rect.x:
            dx = self.speed
        elif portal.rect.x < self.rect.x:
            dx = -self.speed

        if portal.rect.y > self.rect.y:
            dy = self.speed
        elif portal.rect.y < self.rect.y:
            dy = -self.speed

        # collision-safe movement
        self.rect.x += dx
        for p in pillars:
            if self.rect.colliderect(p.rect):
                self.rect.x -= dx

        self.rect.y += dy
        for p in pillars:
            if self.rect.colliderect(p.rect):
                self.rect.y -= dy

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, (200,0,0), self.rect)