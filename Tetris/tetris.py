"""
Tetris is a puzzle video game created by Soviet software 
engineer Alexey Pajitnov in 1984. Built on simple rules 
and requiring intelligence and skill, Tetris established 
itself as one of the great early video games.In Tetris, 
players complete lines by moving differently shaped pieces 
(tetrominoes), which descend onto the playing field. 
The completed lines disappear and grant the player points, 
and the player can proceed to fill the vacated spaces. 
The game ends when the playing field is filled. The longer 
the player can delay this outcome, the higher their score 
will be. 

Tetris is primarily composed of a field of play in which 
pieces of different geometric forms, called "tetrominoes", 
descend from the top of the field. During this descent, 
the player can move the pieces laterally and rotate them 
until they touch the bottom of the field or land on a 
piece that had been placed before it. The player can 
neither slow down the falling pieces nor stop them, but 
can accelerate them in most versions. The objective of the 
game is to use the pieces to create as many horizontal 
lines of blocks as possible. When a line is completed, it 
disappears, and the blocks placed above fall one rank. 
Completing lines grants points, and accumulating a certain 
number of points moves the player up a level, which 
increases the number of points granted per completed line.

In most versions, the speed of the falling pieces 
increases with each level, leaving the player with less 
time to think about the placement. The player can clear 
multiple lines at once, which can earn bonus points in 
some versions. It is possible to complete up to four lines 
simultaneously with the use of the I-shaped tetromino; this 
move is called a "Tetris", and is the basis of the game's 
title. If the player cannot make the blocks disappear 
quickly enough, the field will start to fill, and when the 
pieces reach the top of the field and prevent the arrival 
of additional pieces, the game ends. At the end of each 
game, the player receives a score based on the number of 
lines that have been completed. The game never ends with 
the player's victory; the player can only complete as many 
lines as possible before an inevitable loss.
"""
import pygame
import random
 
# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main
 
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
 
pygame.font.init()
 
# GLOBALS VARIABLES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300  # 10 x 20 grid in tetris, nead to make sure play width is half of play height so we have perfect squares meaning 300 // 10 = 30 width per block. This is the red box being displayed
PLAY_HEIGHT = 600  # meaning 600 // 20 = 20 height per block. This is the red box being displayed
BLOCK_SIZE = 30
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2 # Represents top left position of play area
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT
GREEN = (0, 255, 0) 
RED = (255, 0, 0)
AQUA = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# SHAPE FORMATS
# Find: Regex = \\'(.*)\\'
# Replace: Regex = '$1'
# VSCode regex find and replace video: https://www.youtube.com/watch?v=xMhKstbdr3k
# Geerate regex from text website: https://regex-generator.olafneumann.org/
# VSCode Non-regex find and replace video: https://www.youtube.com/watch?v=sEPN24Sg0SY

# Shape formats represented with list of lists as each 
# shape has possibly more than one orientation (rotate)
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [GREEN, RED, AQUA, YELLOW, ORANGE, BLUE, PURPLE] # index 0 - 6 represent shape 
 
class Tetromino():
    """
    Class representing a tetromino. A tetromino is a 
    geometric shape composed of four squares, connected 
    orthogonally (i.e. at the edges and not the corners).
    """
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0 # Represents orientation of shape
 
def createGrid(locked_positions = {}):
    """Function to create tetris grid"""
    # Create one list for every row in our grid
    # Each of the rows will have 10 columns with
    # colors in them
    grid = [[BLACK for column_index in range(10)] for row_index in range(20)]
    # What if we have some tetrominos that have already 
    # been placed in the grid? We need to draw those 
    # as well. So for whichever positions are occupied
    # by tetrominos we will change its color to the color
    # of the tetromino.
    for row_index in range(len(grid)):
        for column_index in range(len(grid[row_index])):
            if (column_index, row_index) in locked_positions:
                color = locked_positions[(column_index, row_index)]
                grid[row_index][column_index] = color
    return grid

def convertTetrominoFormat(tetromino):
    """"""
    positions = []
    format = tetromino.shape
 
def validTetromino(tetromino, grid):
    pass

def validSpace(tetromino, grid):
    pass
 
def checkLost(positions):
    pass
 
def getTetromino():
    """Function to randomly select next tetromino user will use in tetris"""
    return Tetromino(5, 0, random.choice(shapes))
 
def drawTextMiddle(text, size, color, surface):
    pass
   
def drawGridLines(surface, grid):
    """Function to draw lines on tetris grid"""
    start_x, start_y = TOP_LEFT_X, TOP_LEFT_Y
    for row_index in range(len(grid)):
        pygame.draw.line(surface, GREY, (start_x, start_y + row_index * BLOCK_SIZE), (start_x + PLAY_WIDTH, start_y + row_index * BLOCK_SIZE))
        for column_index in range(len(grid[row_index])):
            pygame.draw.line(surface, GREY, (start_x + column_index * BLOCK_SIZE, start_y), (start_x + column_index * BLOCK_SIZE, start_y + PLAY_HEIGHT))

def clearRows(grid, locked):
    pass
 
def drawNextTetromino(tetromino, surface):
    pass
 
def drawWindow(surface, grid):
    """Function to draw game window"""
    surface.fill(BLACK)
    gamefont = pygame.font.SysFont('comicsans', 60)
    label = gamefont.render('Tetris', 1, WHITE)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH // 2 - (label.get_width() // 2), 30)) # Figure out where middle of screen is
    # Draw the tetris grid
    for row_index in range(len(grid)):
        for column_index in range(len(grid[row_index])):
            pygame.draw.rect(surface, grid[row_index][column_index], (TOP_LEFT_X + column_index * BLOCK_SIZE, TOP_LEFT_Y + row_index * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 4)

    
    drawGridLines(surface, grid)
    pygame.display.update()

def main(win):
    """Main function to run tetris game"""
    locked_positions = {}
    grid = createGrid(locked_positions)
    change_piece = False
    run = True
    current_tetromino = getTetromino()
    next_tetromino = getTetromino()
    clock = pygame.time.Clock()
    fall_time = 0

    # Game Loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Cases we need to handle:
                # 1. Tetromino is moving off the screen 
                # 2. Position is not valid
                if event.key == pygame.K_LEFT:
                    current_tetromino.x -= 1
                    if not validSpace(current_tetromino, grid):
                        current_tetromino.x += 1
                if event.key == pygame.K_RIGHT:
                    current_tetromino.x += 1
                    if not validSpace(current_tetromino, grid):
                        current_tetromino.x -= 1
                if event.key == pygame.K_DOWN:
                    current_tetromino.y += 1
                    if not validSpace(current_tetromino, grid):
                        current_tetromino.y -= 1
                if event.key == pygame.K_UP:
                    current_tetromino.rotation += 1
                    if not validSpace(current_tetromino, grid):
                        current_tetromino.rotation -= 1
            drawWindow(win, grid)

def mainMenu(win):
    """"""
    main(win)
 
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris by @wiknwo')
mainMenu(window)  # start game