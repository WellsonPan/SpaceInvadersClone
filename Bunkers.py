import pygame
from pygame.sprite import Sprite
from pygame import PixelArray

class Bunkers(Sprite):
    def __init__(self, ai_settings, screen):
        super(Bunkers, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        self.image = pygame.image.load("images/Bunker.png")
        self.rect = self.image.get_rect()
        self.hitCount = 0

    def update(self):
        self.pixels = PixelArray(self.image)
        if self.hitCount == 1:
            for i in range(25):
                for j in range(34):
                    self.pixels[i, j] = (0, 0, 0)
        elif self.hitCount == 2:
            for i in range(50, 100):
                for j in range(30, 70):
                    self.pixels[i, j] = (0, 0, 0)
        elif self.hitCount == 3:
            for i in range(50, 100):
                for j in range(70):
                    self.pixels[i, j] = (0, 0, 0)
        elif self.hitCount == 4:
            for i in range(25, 50):
                for j in range(70):
                    self.pixels[i, j] = (0, 0, 0)
        self.pixels.close()

    def drawBunker(self):
        self.screen.blit(self.image, self.rect)

    def updateHitCount(self):
        self.hitCount += 1
