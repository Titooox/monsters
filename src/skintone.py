import pygame

from saveable import Saveable


class SkinTone(Saveable):
    def __init__(self, in_dark: tuple[int], in_light: tuple[int]):
        """Hold onto the darker and lighter colors."""
        self.dark = pygame.Color(in_dark[0], in_dark[1], in_dark[2])
        self.light = pygame.Color(in_light[0], in_light[1], in_light[2])

    def save(self):
        return (self.dark.r, self.dark.g, self.dark.b), (self.light.r, self.light.g, self.light.b)

    @classmethod
    def load(cls, save_data):
        return cls(*save_data)
