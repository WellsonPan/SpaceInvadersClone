import pygame
from pygame.sprite import Sprite
import time

class Alien(Sprite):
    def __init__(self, ai_settings, screen, rowNum):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.rowNum = rowNum

        if rowNum == 0:
            self.skull = ["images/Squid1.png", "images/Squid2.png"]
        elif rowNum == 1:
            self.skull = ["images/Bug1.png", "images/Bug2.png"]
        else:
            self.skull = ["images/Skull1.png", "images/Skull2.png"]
        self.iterate = 0

        self.image = pygame.image.load(self.skull[0])

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.now = time.time()
        self.sec = self.now % 60
        if self.iterate == 0 and (int)(self.sec) % 2 == 1:
            self.image = pygame.image.load(self.skull[1])
            self.iterate = 1
        elif self.iterate == 1 and (int)(self.sec) % 2 == 0:
            self.image = pygame.image.load(self.skull[0])
            self.iterate = 0

        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

class UFO(Sprite):
    def __init__(self, ai_settings, screen):
        super(UFO, self).__init__()
        self.screen = screen
        self.screenRect = screen.get_rect()
        self.ai_settings = ai_settings

        self.image = pygame.image.load("images/UFO.png")

        self.rect = self.image.get_rect()

        if self.ai_settings.ufo_direction == 1:
            self.rect.x = self.screenRect.left - self.rect.width
        else:
            self.rect.x = self.screenRect.right + self.rect.width
        self.rect.y = self.rect.height * 2.5

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += (self.ai_settings.ufo_speed_factor * self.ai_settings.ufo_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.left >= screen_rect.right + (1.5 * self.rect.width):
            return True
        elif self.rect.right <= screen_rect.left - (self.rect.width / 2):
            return True

