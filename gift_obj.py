import random
import pygame

class gift_obj():

    def __init__(self, sprite, loc):
        self.sprite = sprite
        self.loc = loc

    def render(self, surface, scroll):
        surface.blit(self.sprite, (self.loc[0] - scroll[0], self.loc[1]))

    def get_hitbox(self, scroll):
        return pygame.Rect(self.loc[0] - scroll[0], self.loc[1], 16, 16)

    def hitbox_collision(self, hitbox, scroll):
        return self.get_hitbox(scroll).colliderect(hitbox)