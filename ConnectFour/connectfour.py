"""
Connect Four is a two-player connection board game, in 
which the players choose a color and then take turns 
dropping colored tokens into a seven-column, six-row 
vertically suspended grid. The pieces fall straight down, 
occupying the lowest available space within the column. 
The objective of the game is to be the first to form a 
horizontal, vertical, or diagonal line of four of one's 
own tokens. Connect Four is a solved game. The first 
player can always win by playing the right moves.
"""
import numpy as np
import pygame
import sys
import math

# Initializing pygame settings
pygame.font.init()

# Defining constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 80
WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
SCREEN_SIZE = (WIDTH, HEIGHT)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RADIUS = SQUARE_SIZE // 2 - 5
WINNER_FONT = pygame.font.SysFont('monospace', 65)
pygame.display.set_caption('Connect Four') # Change heading in game window

# Functions
def createBoard():
    """Function to create connect four game board"""
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def dropPiece(board, row_index, column_index, piece):
    """Function to drop piece into board"""
    board[row_index][column_index] = piece

def isValidLocation(board, column_index):
    """Function to determine if piece is placed in valid column on board"""
    return board[ROW_COUNT - 1][column_index] == 0 # Checking if top most slot in board is filled or not

def getNextOpenRow(board, column_index):
    """Function to get index of next available row on board"""
    for row_index in range(ROW_COUNT):
        if board[row_index][column_index] == 0:
            return row_index

def printBoard(board):
    """Function to print board in terminal"""
    print(np.flip(board, 0))

def winningMove(board, piece):
    """Function to check for vertical, horizontal or diagonal line of four pieces"""
    # Check for horizontal line of four pieces
    for column_index in range(COLUMN_COUNT - 3):
        for row_index in range(ROW_COUNT):
            if board[row_index][column_index] == piece and board[row_index][column_index + 1] == piece and board[row_index][column_index + 2] == piece and board[row_index][column_index + 3] == piece:
                return True
    
    # Check for vertical line of four pieces
    for column_index in range(COLUMN_COUNT):
        for row_index in range(ROW_COUNT - 3):
            if board[row_index][column_index] == piece and board[row_index + 1][column_index] == piece and board[row_index + 2][column_index] == piece and board[row_index + 3][column_index] == piece:
                return True
    
    # Check for positively sloped diagonals
    for column_index in range(COLUMN_COUNT - 3):
        for row_index in range(ROW_COUNT - 3):
            if board[row_index][column_index] == piece and board[row_index + 1][column_index + 1] == piece and board[row_index + 2][column_index + 2] == piece and board[row_index + 3][column_index + 3] == piece:
                return True

    # Check for negatively sloped diagonals
    for column_index in range(COLUMN_COUNT - 3):
        for row_index in range(3, ROW_COUNT):
            if board[row_index][column_index] == piece and board[row_index - 1][column_index + 1] == piece and board[row_index - 2][column_index + 2] == piece and board[row_index - 3][column_index + 3] == piece:
                return True

def drawBoard(board):
    """Function to draw the connect four board"""
    for column_index in range(COLUMN_COUNT):
        for row_index in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (column_index * SQUARE_SIZE, row_index * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (column_index * SQUARE_SIZE + SQUARE_SIZE // 2, row_index * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
    
    for column_index in range(COLUMN_COUNT):
        for row_index in range(ROW_COUNT):
            if board[row_index][column_index] == 1:
                pygame.draw.circle(screen, RED, (column_index * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - (row_index * SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)
            elif board[row_index][column_index] == 2:
                pygame.draw.circle(screen, YELLOW, (column_index * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - (row_index * SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)
    pygame.display.update()  

board = createBoard()
printBoard(board)
game_over = False
turn = 0
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
drawBoard(board)
pygame.display.update()

# Game Loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # Enabling feature to allow user's piece to hover above board
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            mouse_x_coord = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (mouse_x_coord, SQUARE_SIZE // 2), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (mouse_x_coord, SQUARE_SIZE // 2), RADIUS)
        pygame.display.update() 
        # Tracking which column user has placed piece into
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            # Check if game is a draw
            if np.count_nonzero(board) == ROW_COUNT * COLUMN_COUNT:
                label = WINNER_FONT.render('Draw!', 1, WHITE)
                screen.blit(label, (0, 0))
                game_over = True
            # Ask for player 1 input
            elif turn == 0:
                mouse_x_coord = event.pos[0]
                column_index = math.floor(mouse_x_coord // SQUARE_SIZE)
                if isValidLocation(board, column_index):
                    row_index = getNextOpenRow(board, column_index)
                    dropPiece(board, row_index, column_index, 1)
                    if winningMove(board, 1):
                        label = WINNER_FONT.render('Player 1 wins!', 1, RED)
                        screen.blit(label, (0, 0))
                        game_over = True
            # Ask for player 2 input
            elif turn == 1:
                mouse_x_coord = event.pos[0]
                column_index = math.floor(mouse_x_coord // SQUARE_SIZE)
                if isValidLocation(board, column_index):
                    row_index = getNextOpenRow(board, column_index)
                    dropPiece(board, row_index, column_index, 2)
                    if winningMove(board, 2):
                        label = WINNER_FONT.render('Player 2 wins!', 1, YELLOW)
                        screen.blit(label, (0, 0))
                        game_over = True
            printBoard(board)
            drawBoard(board)
            turn += 1
            turn = turn % 2
            if game_over:
                pygame.time.wait(3000)