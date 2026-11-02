# This file contains the code for the green barrier obstacles, consisting of a Barrier class, and a create_barriers function.

import pygame

# Barrier class representing the green barriers object

class Barrier(pygame.sprite.Sprite):

    # Constructor method assigning attributes and barrier size

    def __init__(self, x, y):
        super().__init__()
        self.health = 10 # health is 10 so barriers are destroyed after 10 hits
        self.colour = "#26FF00" # colour is light green so it can change colour without getting too dark
        self.width = 66 # width is 600/9 and rounded down to allow for 4 barriers with 5 equally spaced gaps
        self.height = 33 # height is half the width to create a rectangle
        self.rect = pygame.Rect(0, 0, self.width, self.height) # assign current barrier size
        self.rect.center = (x,y) # assign current barrier centre

    # Method changing size and colour of barriers when hit    

    def hit(self):
        self.health -= 1 # decrementing health by 1 each time the barrier is hit
        self.width -= 66/18 # decrementing width by 66/18 so barrier width is half its original size after 9 hits and destroyed after 10
        self.height -= 33/18 # decrementing height by 33/18 so barrier height is half its original size after 9 hits and destroyed after 10
        old_centre = self.rect.center # assign the current centre value to this to save it before updating barrier size
        self.rect = pygame.Rect(0, 0, int(self.width), int(self.height)) # update the current barrier size
        self.rect.center = old_centre # assign updated barrier centre

        if self.health == 8: self.colour = "#3EA521" # barrier colour updated to medium green colour after 2 hits
        elif self.health == 6: self.colour = "#35582C" # barrier colour updated to darker green colour after 4 hits
        elif self.health == 4: self.colour = "#FF8A04" # barrier colour updated to orange colour after 6 hits
        elif self.health == 2: self.colour = "#FF0000" # barrier colour updated to red colour after 8 hits
        elif self.health <= 0: self.kill() # barrier destroyed after 10 hits

    # Method drawing the barrier by passing in screen from main.py as a parameter   

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect) # drawing the barrier colour and shape onto the screen

# Function creating the barriers by calculating gap and barrier centre

def create_barriers(screen_width, screen_height):
    gap = (screen_width - (4 * 66))/5 # calculate gap by subtracting the width of 4 barriers from screen width, sharing 5 equally spaced gaps
    barriers = [] # barriers are stored in an empty list
    for i in range(4): # for loop, running once per barrier, 4 times in total
        offset_x = ((i + 1) * gap) + (i * 66 + 33) # calculate x value centre by adding gaps before it to barriers before it plus half a barrier
        barrier = Barrier(offset_x, screen_height - 200) # Barrier object subtracting 200 to calculate y value centre
        barriers.append(barrier) # adds this one barrier to the list with .append
    
    return barriers # send list back to main.py

