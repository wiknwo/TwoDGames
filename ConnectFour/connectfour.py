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

# Defining constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 80
WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
SCREEN_SIZE = (WIDTH, HEIGHT)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RADIUS = SQUARE_SIZE // 2 - 5

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
    for row_index in range(ROW_COUNT):
        if board[row_index][column_index] == 0:
            return row_index

def printBoard(board):
    print(np.flip(board, 0))

def winningMove(board, piece):
    """Check for vertical, horizontal or diagonal line of four pieces"""
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
    """Function to darw the connect four board"""
    for column_index in range(COLUMN_COUNT):
        for row_index in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (column_index * SQUARE_SIZE, row_index * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (column_index * SQUARE_SIZE + SQUARE_SIZE // 2, row_index * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
            # Ask for player 1 input
            # if turn == 0:
            #     column_index = int(input("Player 1 Make your selection (0 - 6):"))
            #     if isValidLocation(board, column_index):
            #         row_index = getNextOpenRow(board, column_index)
            #         dropPiece(board, row_index, column_index, 1)
            #         if winningMove(board, 1):
            #             print("Player 1 wins!")
            #             game_over = True
            # # Ask for player 2 input
            # else:
            #     column_index = int(input("Player 2 Make your selection (0 - 6):"))
            #     if isValidLocation(board, column_index):
            #         row_index = getNextOpenRow(board, column_index)
            #         dropPiece(board, row_index, column_index, 2)
            #         if winningMove(board, 2):
            #             print("Player 2 wins!")
            #             game_over = True
            # printBoard(board)
            # turn += 1
            # turn = turn % 2