"""
Tic-tac-toe (American English), noughts and crosses 
(Commonwealth English), or Xs and Os (Irish English) is a 
paper-and-pencil game for two players who take turns 
marking the spaces in a three-by-three grid with X or O. 
The player who succeeds in placing three of their marks in 
a horizontal, vertical, or diagonal row is the winner. It 
is a solved game, with a forced draw assuming best play 
from both players.
"""
import random

# Game variables
board = [' ' for i in range(10)] # Want one leading space in board

# Functions
def insertLetter(letter, position):
    """Function to insert letter into board list"""
    board[position] = letter

def spaceIsFree(position):
    """Function to check if position is free for insertion"""
    return board[position] == ' '

def printBoard(board):
    """Function to print board in visually pleasing way"""
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')    
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')    
    print('-----------')
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')

def isWinner(board, letter):
    """Function to check if we have winner based on our current board"""
    horizontals = (board[7] == letter and board[8] == letter and board[9] == letter) or (board[4] == letter and board[5] == letter and board[6] == letter) or (board[1] == letter and board[2] == letter and board[3] == letter)
    verticals = (board[1] == letter and board[4] == letter and board[7] == letter) or (board[2] == letter and board[5] == letter and board[8] == letter) or (board[3] == letter and board[6] == letter and board[9] == letter)
    diagonals = (board[1] == letter and board[5] == letter and board[9] == letter) or (board[3] == letter and board[5] == letter and board[7] == letter)
    return horizontals or verticals or diagonals

def playerMove():
    """Function to model a move made by the human player"""
    run = True
    while run:
        move = input('Please select a position to place an \'X\' (1 - 9): ')
        try:
            move = int(move)
            if move > 0 and move < 10:
                if spaceIsFree(move):
                    run = False
                    insertLetter('X', move)
                else:
                    print('Sorry, this space is occupied!')
            else:
                print('Please type a number within the range!')
        except:
            print('Please type a number')

def computerMove():
    """
    Function to determine computer's move
    1. Is there a move we can do that results in us winning. If there is, let's make that move
    2. We can't win on the move, is there a move that the player can make on their next turn that will make them win the game, if we find that move; we will prevent the player making it by moving into that position
    3. I can't win, the player can't win so it's not that important where we move so we will pick a corner to move to.
    4. If there are no corners free then we will take the centre
    5. Move to any open edge
    """
    possible_moves = [i for i, letter in enumerate(board) if letter == ' ' and i != 0]
    move = 0 # Default move
    # Make copy of board, check every single empty position 
    # and see if when we move into each empty position if 
    # it's a winning position or not. Steps 1 and 2.
    for letter in ['O', 'X']:
        for i in possible_moves:
            board_copy = board[:] # Make a copy of the board
            board_copy[i] = letter
            if isWinner(board_copy, letter):
                move = i
                return move
    # Step 3
    open_corners = []
    for i in possible_moves:
        if i in [1, 3, 7, 9]:
            open_corners.append(i)
    if len(open_corners) > 0:
        move = selectRandom(open_corners)
        return move
    # Step 4
    if 5 in possible_moves:
        move = 5
        return move
    # Step 5
    open_edges = []
    for i in possible_moves:
        if i in [2, 4, 6, 8]:
            open_edges.append(i)
    if len(open_edges) > 0:
        move = selectRandom(open_edges)
    return move
    
def selectRandom(lst):
    """Function to select random index of given list"""
    return lst[random.randrange(0, len(lst))]


def isBoardFull(board):
    """Function to check if the board is full"""
    return False if board.count(' ') > 1 else True

def main():
    """Function to run Tic Tac Toe game"""
    print('Welcome to Tic Tac Toe!')
    printBoard(board)
    # Game loop
    while not isBoardFull(board):
        # Checking if computer won
        if not isWinner(board, 'O'):
            playerMove()
            printBoard(board)
        else:
            print('Sorry, O\'s won this time!')
            break
        # Checking if player won
        if not isWinner(board, 'X'):
            move = computerMove()
            if move == 0:
                print('Tie Game!')
            else:
                insertLetter('O', move)
                print('Compluter placed an \'O\' in position', move, ':')
                printBoard(board)
        else:
            print('Sorry, X\'s won this time!')
            break

    if isBoardFull(board):
        print('Tie Game!')

if __name__ == '__main__':
    main()