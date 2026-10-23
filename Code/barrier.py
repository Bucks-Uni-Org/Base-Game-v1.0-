# This file, barrier.py is for the green barriers, which are obstacles in the space invaders game
# I used a YouTube video to assist me in developing this code
# The channel name is: Programming With Nick
# The video title is: Python Space Invaders Game Tutorial with Pygame - Beginner Tutorial (OOP)
# The video link is: https://youtu.be/PFMoo_dvhyw?si=qv6VuKC9bzzJo65L
# Things I adapted: list comprehension, hex colour method instead of rgb, colour and shape of barrier, class names.

import pygame

# Pixel class

class Pixel(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.image = pygame.Surface((3,3))
        self.image.fill(("#39FF14"))
        self.rect = self.image.get_rect(topleft = (x,y))

# Grid - shape of barriers        

grid = [
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
[1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]]

# Barrier class

class Barrier:
    def __init__(self, x, y):
        self.pixel_group = pygame.sprite.Group()
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column] == 1:
                    pos_x = x + column * 3
                    pos_y = y + row * 3
                    pixel = Pixel(pos_x, pos_y)
                    self.pixel_group.add(pixel)