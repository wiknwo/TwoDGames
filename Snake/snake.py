"""
Snake is a video game genre where the player maneuvers a 
growing line that becomes a primary obstacle to itself. 
The concept originated in the 1976 two-player arcade game 
Blockade from Gremlin Industries, and the ease of 
implementation has led to hundreds of versions (some of 
which have the word snake or worm in the title) for many 
platforms. 1982's Tron arcade game, based on the film, 
includes snake gameplay for the single-player Light Cycles 
segment. After a variant was preloaded on Nokia mobile 
phones in 1998, there was a resurgence of interest in 
snake games as it found a larger audience.

The player controls a dot, square, or object on a bordered 
plane. As it moves forward, it leaves a trail behind, 
resembling a moving snake. The player loses when the snake 
runs into the screen border, other obstacle, or itself.

The snake has a specific length, so there is a moving tail 
a fixed number of units away from the head. A sole player 
attempts to eat items by running into them with the head 
of the snake. Each item eaten makes the snake longer, so 
avoiding collision with the snake becomes progressively 
more difficult.
"""
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Cube():
    """
    Class representing snack eaten by snake

    Attributes:
    """
    rows, width = 0, 0

    def __init__(self, start, dirnx=2, dirny=0, color=(255, 0, 0)):
        pass

    def move(self, dirnx, dirny):
        pass

    def draw(self, surface, eyes=False):
        pass

class Snake():
    """
    Class representing snake

    Attributes:
    """
    def __init__(self, color, pos):
        pass

    def move(self):
        pass

    def reset(self, pos):
        pass

    def addCube(self):
        pass
    
    def draw(self, surface):
        pass

def drawGrid(width, rows, surface):
    """
    We are going to figure out how big each square in the grid
    is going to be. What we will do is draw lines down and across
    but we need to figure out where to draw those lines. So
    we have to figure out the gap between each of the lines
    """
    gapbetweenlines = width // rows
    x, y = 0, 0
    for i in range(rows):
        x += gapbetweenlines
        y += gapbetweenlines
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width)) # Draw vertical line
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y)) # Draw horizontal line

def redrawWindow(surface):
    """"""
    global rows, width
    surface.fill((0, 0, 0))
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, items):
    """"""
    pass

def message_box(subject, content):
    """"""
    pass

def main():
    """Main function to run Snake game"""
    # Setting up window
    global width, rows
    width = 500 # Dimensions of square shaped grid
    rows = 20 # Denotes how many rows and columns we will have on the grid. Can be set to any value that divides width and height evenly otherwise rows and columns will look awkward. Also determines room for snake to move around
    window = pygame.display.set_mode((width, width))
    s = Snake((255, 0, 0), (10, 10))
    flag = True
    clock = pygame.time.Clock()

    # Game Loop
    while flag:
        # Setting speed of game: Settings are machine dependent
        pygame.time.delay(50) # Delays 50 milliseconds every time so program doesn't run too fast. The lower this goes, the faster the game will be.
        clock.tick(10) # Ensures game doesn't run more than 10 frames per second. The lower this goes, the slower the game will be.
        redrawWindow(window)

if __name__ == '__main__':
    main()