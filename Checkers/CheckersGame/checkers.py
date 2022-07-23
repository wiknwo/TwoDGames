"""
Checkers, also known as draughts, is a group of strategy 
board games for two players which involve diagonal moves 
of uniform game pieces and mandatory captures by jumping 
over opponent pieces. Checkers is developed from alquerque.
The term "checkers" derives from the checkered board which 
the game is played on, whereas "draughts" derives from the 
verb "to draw" or "to move".

The most popular forms of checkers in Anglophone countries 
are American checkers (also called English draughts), 
which is played on an 8x8 checkerboard; Russian draughts, 
Turkish draughts both on an 8x8 board, and International 
draughts, played on a 10x10 board - the latter is widely 
played in many countries worldwide. 

Checkers is played by two opponents on opposite sides of 
the game board. One player has the dark pieces (usually black); 
the other has the light pieces (usually white or red). 
Players alternate turns. A player cannot move an opponent's 
pieces. A move consists of moving a piece diagonally to an 
adjacent unoccupied square. If the adjacent square 
contains an opponent's piece, and the square immediately 
beyond it is vacant, the piece may be captured (and removed 
from the game) by jumping over it.

Only the dark squares of the checkerboard are used. A 
piece can only move diagonally into an unoccupied square. 
When capturing an opponent's piece is possible, capturing 
is mandatory in most official rules. If the player does 
not capture, the other player can remove the opponent's 
piece as penalty (or muffin). And where there are two or 
more such positions, the player forfeits pieces that 
cannot be moved. Although some rule variations make 
capturing optional. In almost all variants, the player 
without pieces remaining, or who cannot move due to being 
blocked, loses the game.
"""
import pygame
from pycheckers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED
from pycheckers.game import Game

# Setting up pygame display
FRAMES_PER_SECOND = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers by @wiknwo')

# Functions
def getRowColumnFromMouse(position):
    """Function to get row and column from mouse position"""
    x, y = position
    row = y // SQUARE_SIZE
    column = x // SQUARE_SIZE
    return row, column

# Game loop
def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)

    while run:
        clock.tick(FRAMES_PER_SECOND)
        if game.winner() != None:
            print(game.winner())
            run = False
            pygame.time.wait(3000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                row, column = getRowColumnFromMouse(mouse_position)
                game.select(row, column)
        game.update()
    pygame.quit()

if __name__ == '__main__':
    main()