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
    """Class representing snack eaten by snake"""
    rows, width = 20, 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        """Initializes Cube variables"""
        self.position = start
        self.direction_x = 1 # Set to 1 so that snake is moving upon program start. If it wasn't set then that would mean user would have to click a button to start moving.
        self.direction_y = 0
        self.color = color

    def move(self, dirnx, dirny):
        """Method to move cube in given direction"""
        self.direction_x = dirnx
        self.direction_y = dirny
        self.position = (self.position[0] + self.direction_x, self.position[1] + self.direction_y)

    def draw(self, surface, eyes=False):
        """
        Method to draw cube on screen. Need to figure out 
        distance between each x and y value for each cube. 
        Pygame draws in the top left hand corner of the object
        """
        distance = self.width // self.rows
        i, j = self.position[0], self.position[1] # row, column
        pygame.draw.rect(surface, self.color, (i * distance + 1, j * distance + 1, distance - 2, distance - 2)) # + 1, - 2 is just so we can still see the grid when we draw the rectangle. If we were to draw with exact dimensions of the grid we would cover the white lines (+1). (-2) So that we are drawing inside the square grid a little bit.
        # Drawing the eyes on the cube
        if eyes:
            centre = distance // 2
            radius = 3
            circle_midde = (i * distance + centre - radius, j * distance + 8)
            circle_midde2 = (i * distance + distance - radius * 2, j * distance + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_midde, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_midde2, radius)

class Snake():
    """Class representing snake"""
    # Defining static variables
    body = [] # List of cube representing snake body
    turns = {}

    def __init__(self, color, position):
        """Initialize variables for snake object"""
        self.color = color
        self.head = Cube(position)
        self.body.append(self.head)
        self.direction_x, self.direction_y = 0, 1 # These direction variables will be in the range [-1, 1] and will keep track of which direction we are moving in

    def move(self):
        """Method to move snake in direction indicated by user"""
        # Checking if user is pressing directional keys 
        # to change direction of snake. Using if-elif 
        # statements because we don't want user to click
        # more than one key at once
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Ensures user can quit game by clicking red x in window
                pygame.quit()
            
            keys = pygame.key.get_pressed() # Returns a dict of all key values and if they were pressed or not
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.direction_x = -1 # Change direction of snake to move left
                    self.direction_y = 0 # Leave y direction unchanged as we don't want snake to move in two directions simultaneously
                    # We need to remember where we 
                    # turned so the tail of the snake can 
                    # turn at that point.
                    self.turns[self.head.position[:]] = [self.direction_x, self.direction_y] # key: current position of head of snake, value: direction snake turned in
                elif keys[pygame.K_RIGHT]:
                    self.direction_x = 1 # Change direction of snake to move right
                    self.direction_y = 0 
                    self.turns[self.head.position[:]] = [self.direction_x, self.direction_y] # key: current position of head of snake, value: direction snake turned in
                elif keys[pygame.K_UP]:
                    self.direction_x = 0 
                    self.direction_y = -1 # In pygame, a negative y value corresponds to moving upwards
                    self.turns[self.head.position[:]] = [self.direction_x, self.direction_y] # key: current position of head of snake, value: direction snake turned in
                elif keys[pygame.K_DOWN]:
                    self.direction_x = 0 
                    self.direction_y = 1 # In pygame, a positive y value corresponds to moving downward
                    self.turns[self.head.position[:]] = [self.direction_x, self.direction_y] # key: current position of head of snake, value: direction snake turned in
        # Move the cube: Looking at where the cube is and 
        # if it is at the turn then we will turn the cube
        for i, cube in enumerate(self.body):
            p = cube.position[:] # Creates a copy of the position so we are not changing the position of the snake when we do this
            if p in self.turns: # Checking if the cube's position is at the position of a turn
                turn = self.turns[p]
                cube.move(turn[0], turn[1])
                # If we are at the last cube in the body 
                # then we will remove that cube. If we 
                # didn't it would mean that any time the snake
                # hit that position on the screen regardless of
                # whether the snake were to turn or not 
                # you would automatically change directions.
                if i == len(self.body) - 1:
                    self.turns.pop(p) 
            else:
                # Boundary checking: See if we are at the edge of the screen.
                if cube.direction_x == -1 and cube.position[0] <= 0:
                    # If we are moving left and the x coordinate of the cube <= 0 i.e. edge of the screen
                    # then we will change that position so it goes to the right side
                    # of the screen.
                    cube.position = (cube.rows - 1, cube.position[1])
                elif cube.direction_x == 1 and cube.position[0] >= cube.rows - 1:
                    # If we are moving right and the x coordinate of the cube >= cube.rows - 1 i.e. edge of the screen
                    # then move back to the left side
                    cube.position = (0, cube.position[1])
                elif cube.direction_y == 1 and cube.position[1] >= cube.rows - 1:
                    # If we are moving down and the y coordinate >= cube.rows - 1 i.e. edge of the screen
                    # then move us back to the top
                    cube.position = (cube.position[0], 0)
                elif cube.direction_y == -1 and cube.position[1] <= 0:
                    # If we are moving up and the y coordinate <= 0 i.e. edge of the screen
                    # then move us back to the bottom
                    cube.position = (cube.position[0], cube.rows - 1)
                else:
                    cube.move(cube.direction_x, cube.direction_y) # If we are not at the edge of the screen then we will move the cube in the same direction it was going in before.

    def reset(self, position):
        """Method to get rid of body, turns, direction_x and direction_y"""
        self.head = Cube(position)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction_x, self.direction_y = 0, 1 # Set to 1 so snake is moving on game start

    def addCube(self):
        """Method to add cube to snake body"""
        tail = self.body[-1]
        dx, dy = tail.direction_x, tail.direction_y
        # Checking which direction the tail is moving in so we can add a cube accordingly
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.position[0] - 1, tail.position[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.position[0] + 1, tail.position[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.position[0], tail.position[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.position[0], tail.position[1] + 1)))
        # Set direction for added cube so that it moves with snake body
        # Wherever the tail is moving that is where the added cube is going to be moving
        self.body[-1].direction_x = dx
        self.body[-1].direction_y = dy

    def draw(self, surface):
        """Method to draw snake body on screen"""
        for i, cube in enumerate(self.body):
            if i == 0:
                cube.draw(surface, True) # Draw eyes onto the head of the snake only
            else:
                cube.draw(surface)

def drawGrid(width, rows, surface):
    """
    Method to draw grid with rows in game window. We are 
    going to figure out how big each square in the grid
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
    """Method to redraw game window"""
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, snake):
    """Method to generate random snack on screen that snake can eat"""
    positions = snake.body
    while True:
        x, y = random.randrange(rows), random.randrange(rows)
        # Getting a list of a filtered list and seeing if any
        # of the positions is the same as the current position
        # of the snake i.e. trying not to put a snack on top 
        # of the snake
        if len(list(filter(lambda z:z.position == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

def message_box(subject, content):
    """Method to generate message box pop up indicating user about status of game"""
    root = tk.Tk()
    root.attributes("-topmost", True) # Ensuring message box shows up on top of everything so that if many windows are open it will show up on top of them
    root.withdraw() # Make message box invisible
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    """Main function to run Snake game"""
    # Setting up window
    global width, rows, s, snack
    width = 500 # Dimensions of square shaped grid
    rows = 20 # Denotes how many rows and columns we will have on the grid. Can be set to any value that divides width evenly otherwise rows and columns will look awkward. Also determines room for snake to move around.
    window = pygame.display.set_mode((width, width))
    s = Snake((255, 0, 0), (10, 10))
    snack = Cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True
    clock = pygame.time.Clock()

    # Game Loop
    while flag:
        # Setting speed of game: Settings are machine dependent
        pygame.time.delay(50) # Delays 50 milliseconds every time so program doesn't run too fast. The lower this goes, the faster the game will be.
        clock.tick(10) # Ensures game doesn't run more than 10 frames per second. The lower this goes, the slower the game will be.
        s.move()
        # Checking if head of snack hit snack, if it does 
        # we add another cube to the body of the snake.
        if s.body[0].position == snack.position:
            s.addCube()
            snack = Cube(randomSnack(rows, s), color=(0, 255, 0))
        # Checking for snake body colliding with itself
        for i in range(len(s.body)):
            if s.body[i].position in list(map(lambda z:z.position, s.body[i + 1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10, 10))
                break
        redrawWindow(window)

if __name__ == '__main__':
    main()