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
    format = tetromino.shape[tetromino.rotation % len(tetromino.shape)]
    # 
    for row_index, line in enumerate(format):
        row = list(line)
        for column_index, character in enumerate(row):
            if character == '0':
                positions.append((tetromino.x + column_index, tetromino.y + row_index))
    # 
    for i, position in enumerate(positions):
        positions[i] = (position[0] - 2, position[1] - 4) # Moving everything to the left and up so when we are displaying everything looks accurate
    
    return positions

def validSpace(tetromino, grid):
    """"""
    accepted_positions = [[(column_index, row_index) for column_index in range(10) if grid[row_index][column_index] == BLACK] for row_index in range(20)] # Only add to accepted positions if its empty, otherwise a tetromino is occupying the position.
    accepted_positions = [column_index for sublist in accepted_positions for column_index in sublist]
    formatted = convertTetrominoFormat(tetromino)
    for position in formatted:
        if position not in accepted_positions:
            if position[1] > -1: # Because of offset, sometimes positions will be negative and we need to account for that
                return False
    return True
 
def checkLost(positions):
    """Function to check if any of the tetrominos are above the screen"""
    for position in positions:
        x, y = position
        if y < 1:
            return True
    return False
 
def getTetromino():
    """Function to randomly select next tetromino user will use in tetris"""
    return Tetromino(5, 0, random.choice(shapes))
 
def drawTextMiddle(text, size, color, surface):
    """Function to draw text in centre of screen"""
    font = pygame.font.SysFont('comicsans', size, bold = True)
    label = font.render(text, 1, color)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH // 2 - (label.get_width() // 2), TOP_LEFT_Y + PLAY_HEIGHT // 2 - (label.get_height() // 2)))
   
def drawGridLines(surface, grid):
    """Function to draw lines on tetris grid"""
    start_x, start_y = TOP_LEFT_X, TOP_LEFT_Y
    for row_index in range(len(grid)):
        pygame.draw.line(surface, GREY, (start_x, start_y + row_index * BLOCK_SIZE), (start_x + PLAY_WIDTH, start_y + row_index * BLOCK_SIZE))
        for column_index in range(len(grid[row_index])):
            pygame.draw.line(surface, GREY, (start_x + column_index * BLOCK_SIZE, start_y), (start_x + column_index * BLOCK_SIZE, start_y + PLAY_HEIGHT))

def clearRows(grid, locked_positions):
    """Function to clear row if user gets a line"""
    inc = 0
    for row_index in range(len(grid) - 1, -1, -1):
        row = grid[row_index]
        if BLACK not in row:
            inc += 1
            ind = row_index
            # Clear row
            for column_index in range(len(row)):
                try:
                    del locked_positions[(column_index, row_index)]
                except:
                    continue
    # Shift rows since we have cleared a row
    if inc > 0:
        # For every key in our sorted list of locked positions
        # based on the y value
        for key in sorted(list(locked_positions), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind: # If y is above current index of row we removed
                new_key = (x, y + inc)
                locked_positions[new_key] = locked_positions.pop(key)
    return inc

def drawNextTetromino(tetromino, surface):
    """Function to draw the next tetromino on the screen to show the user"""
    font = pygame.font.SysFont('comicsans', 25)
    label = font.render('Next Tetromino', 1, WHITE)
    start_x = TOP_LEFT_X + PLAY_WIDTH + 20
    start_y = TOP_LEFT_Y + PLAY_HEIGHT // 2 - 100
    format = tetromino.shape[tetromino.rotation % len(tetromino.shape)]
    for row_index, line in enumerate(format):
        row = list(line)
        for column_index, character in enumerate(row):
            if character == '0':
                pygame.draw.rect(surface, tetromino.color, (start_x + column_index * BLOCK_SIZE, start_y + row_index * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    surface.blit(label, (start_x + 10, start_y - 30))

def drawWindow(surface, grid, score = 0):
    """Function to draw game window"""
    surface.fill(BLACK)
    gamefont = pygame.font.SysFont('comicsans', 60)
    label = gamefont.render('Tetris', 1, WHITE)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH // 2 - (label.get_width() // 2), 0)) # Figure out where middle of screen is
    # Draw the score
    scorefont = pygame.font.SysFont('comicsans', 25)
    label = scorefont.render('Score: ' + str(score), 1, WHITE)
    start_x = TOP_LEFT_X + PLAY_WIDTH + 20
    start_y = TOP_LEFT_Y + PLAY_HEIGHT // 2 - 100
    surface.blit(label, (start_x + 20, start_y + 160))
    # Draw the tetris grid
    for row_index in range(len(grid)):
        for column_index in range(len(grid[row_index])):
            pygame.draw.rect(surface, grid[row_index][column_index], (TOP_LEFT_X + column_index * BLOCK_SIZE, TOP_LEFT_Y + row_index * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 4)
    drawGridLines(surface, grid)

def main(win):
    """Main function to run tetris game"""
    pygame.init()
    locked_positions = {} # key: position (x, y), value: color (r, g, b)
    grid = createGrid(locked_positions)
    change_piece = False
    run = True
    current_tetromino = getTetromino()
    next_tetromino = getTetromino()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0 
    score = 0

    # Game Loop
    while run:
        grid = createGrid(locked_positions) # Every time we move there is a chance we will add to locked positions
        fall_time += clock.get_rawtime() # Gets the amount of time since last clock.tick
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5: # Greater than 5 seconds
            level_time = 0
            if level_time > 0.15:
                level_time -= 0.005
        
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_tetromino.y += 1
            # Handle case where tetromino hits bottom of screen
            if not validSpace(current_tetromino, grid) and current_tetromino.y > 0:
                # If we are moving down and we move into a position
                # that is not valid that means we know we didn't move left or right 
                # off the screen because we are moving down 
                # so it means we hit the bottom of the screen or 
                # moved into another tetromino. So, stop moving 
                # this tetromino and change it to the next one.
                current_tetromino.y -= 1
                change_piece = True 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
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
            
            # Check all positions of shape moving down to see
            # if we've hit the ground or see if we need to lock it
            shape_positions = convertTetrominoFormat(current_tetromino)
            for i in range(len(shape_positions)):
                x, y = shape_positions[i]
                if y > -1: # Means we are not above the screen
                    grid[y][x] = current_tetromino.color
            # 
            if change_piece:
                # Locked position: (i) Tetromino is no longer moving
                # (ii) Tetromino hit bottom of the screen. Updating
                # grid with positions that have now been occupied.
                for position in shape_positions:
                    key = (position[0], position[1])
                    locked_positions[key] = current_tetromino.color
                current_tetromino = next_tetromino
                next_tetromino = getTetromino()
                change_piece = False
                score += clearRows(grid, locked_positions) * 10
            
            drawWindow(win, grid, score)
            drawNextTetromino(next_tetromino, win)
            pygame.display.update()
            # Checking if user has lost game
            if checkLost(locked_positions):
                drawTextMiddle("YOU LOST!", 80, WHITE, win)
                pygame.display.update()
                pygame.time.delay(1500)
                run = False

def displayMainMenu(win):
    """Function to make main menu popup when user hits any key"""
    run = True
    while run:
        win.fill(BLACK)
        drawTextMiddle('Press Any Key To Play', 60, WHITE, win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.display.quit()
    
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris by @wiknwo')
displayMainMenu(window)  # start game