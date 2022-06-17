"""
Game of Life, also known simply as Life, is a cellular 
automaton devised by the British mathematician John Horton 
Conway in 1970. It is a zero-player game, meaning that its 
evolution is determined by its initial state, requiring no 
further input. One interacts with the Game of Life by 
creating an initial configuration and observing how it 
evolves. 

The universe of the Game of Life is an infinite, 
two-dimensional orthogonal grid of square cells, each of 
which is in one of two possible states, live or dead (or 
populated and unpopulated, respectively). Every cell 
interacts with its eight neighbours, which are the cells 
that are horizontally, vertically, or diagonally adjacent.
At each step the following transistions occur:

1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

The initial pattern constitutes the seed of the system. The 
first generation is created by applying the above rules 
simultaneously to every cell in the seed, live or dead; 
births and deaths occur simultaneously, and the discrete 
moment at which this happens is sometimes called a tick. Each 
generation is a pure function of the preceding one. The 
rules continue to be applied repeatedly to create further 
generations.
"""
import time
import pygame
import numpy as np

"""Define basic colors as we will be reusing them frequently"""
COLOR_BACKGROUND = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170) # Color for cell that will die in next generation
COLOR_ALIVE_NEXT = (255, 255, 255) # Color for cell that will be alive in next generation

def update(screen, cells, size, with_progress=False):
    """
    This method contains whole game logic and drawing processes

    Params:
        screen: Ordinary pygame screen object
        cells: Playing field containing state of individual cells
        size: size of individual cell
        with_progress: Boolean indicating whether we want to move to the next generation
    """
    updated_cells = np.zeros((cells.shape[0], cells.shape[1])) # Takes the shape of already existing cells object and creates an empty numpy array of the same shape
    for row, column in np.ndindex(cells.shape):
        # Calculate number of neighbours of current cell that are alive
        alive = np.sum(cells[row - 1: row + 2, column - 1:column + 2]) - cells[row, column]
        color = COLOR_BACKGROUND if cells[row, column] == 0 else COLOR_ALIVE_NEXT
        # Implement game rules
        if cells[row, column] == 1:
            if alive < 2 or alive > 3: # Cell dies due to underpopulation or overpopulation
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif alive == 2 or alive == 3: # Cell lives onto next generation
                updated_cells[row, column] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3: # Dead cell comes to life as if by reproduction
                updated_cells[row, column] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        # Drawing the individual pixels in specified color.
        # Individual cell has a certain size so we need to go
        # as many cells as columns to the right and as many rows
        # as cells down.
        pygame.draw.rect(screen, color, (column * size, row * size, size - 1, size - 1))
    return updated_cells

def main():
    """Main function to run Conway's Game of Life simulation"""
    # Initialize Game 
    pygame.init() # Initialize pygame
    screen = pygame.display.set_mode((800, 600)) # Set up screen
    # Fill screen with grid
    cells = np.zeros((60, 80)) # Must flip the cells to function correctly, [60, 80] not [80, 60]. Initially there are no cells we only have zeros
    screen.fill(COLOR_GRID) # Fill the screen with grid color as background. Go to each individual cell and fill it with background color unless we have reason not to
    update(screen, cells, 10) # Initially calling the update method with with_progress parameter set to False
    #
    pygame.display.flip()
    pygame.display.update() # Update the contents of the entire display
    #
    running = False # Flag indicating if game is in motion
    # Game Loop: We will be polling the user for key inputs
    # If we notice user presses the space button then running 
    # will be set to true and this will trigger the update method
    # to called with_progress = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]: # Adding cells by using mouse
                # If mouse is pressed we want to know the co-ordinates of the mouse press. Where was it pressed?
                position = pygame.mouse.get_pos()
                cells[position[1] // 10, position[0] // 10] = 1 # Set cell at mouse position to 1
                update(screen, cells, 10)
                pygame.display.update()
        screen.fill(COLOR_GRID) # Every time we must fill the screen again
        # Handling scenario where we want to show progress
        if running:
            cells = update(screen, cells, 10, True)
            pygame.display.flip()
        time.sleep(0.001) 

if __name__ == '__main__':
    main()