import pygame
import pygame.font

class Start():
    def __init__(self, pongSettings, screen):
        self.pongSettings = pongSettings
        self.screen = screen

        self.rect = pygame.Rect(0, 0, pongSettings.screenWidth, pongSettings.screenHeight)
        self.screenRect = screen.get_rect()
        self.text_color = (255, 255, 255)
        self.text_color_2 = (0, 255, 0)

        self.color = pongSettings.backgroundColor

        self.prep_msg("Space", "Invaders")

    def prep_msg(self, msg, msg2):
        self.font = pygame.font.SysFont(None, 200)
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        self.msg_image_rect.centery = self.rect.centery - 300

        self.font = pygame.font.SysFont(None, 100)
        self.msg2_image = self.font.render(msg2, True, self.text_color_2)
        self.msg2_image_rect = self.msg2_image.get_rect()
        self.msg2_image_rect.center = self.rect.center
        self.msg2_image_rect.centery = self.rect.centery - 200

    def printStart(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self.screen.blit(self.msg2_image, self.msg2_image_rect)
