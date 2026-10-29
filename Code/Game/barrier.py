# barrier.py contains the code for the green barrier obstacles in the game space invaders.

import pygame

class Barrier(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.health = 10
        self.colour = "#26FF00"
        self.width = 66
        self.height = 33
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x,y)

    def hit(self):
        self.health -= 1
        self.width -= 66/18
        self.height -= 33/18
        old_center = self.rect.center
        self.rect = pygame.Rect(0, 0, int(self.width), int(self.height))
        self.rect.center = old_center

        if self.health == 8: self.colour = "#3EA521"
        elif self.health == 6: self.colour = "#35582C"
        elif self.health == 4: self.colour = "#FF8A04"
        elif self.health == 2: self.colour = "#FF0000"
        elif self.health <= 0: self.kill()
