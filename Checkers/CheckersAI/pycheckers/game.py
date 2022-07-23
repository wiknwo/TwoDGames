import pygame
from .constants import RED, SQUARE_SIZE, WHITE, BLUE
from .board import Board

class Game:
    """Class to handle game logic and interfacing with board and pieces"""
    def __init__(self, window):
        """Method to initialize game variables"""
        self.__init()
        self.window = window
    
    def update(self):
        """Method to update the game's display"""
        self.board.draw(self.window)
        self.drawValidMoves(self.valid_moves)
        pygame.display.update()

    def __init(self):
        """Private method to intialize game variables"""
        self.selected_piece = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        """Method to call declareWinner() from board class"""
        return self.board.declareWinner()

    def reset(self):
        """Method to reset game variables"""
        self.__init()

    def select(self, row, column):
        """Method to manipulate selected piece"""
        if self.selected_piece:
            result = self.__move(row, column)
            if not result:
                self.selected_piece = None # Reset selection
                self.select(row, column) # Reselect a row and column
                  
        piece = self.board.getPiece(row, column)
        if piece != 0 and piece.color == self.turn:
            self.selected_piece = piece
            self.valid_moves = self.board.getValidMoves(piece)
            return True
        return False

    def __move(self, row, column):
        """Private method to attempt to move piece to valid position"""
        piece = self.board.getPiece(row, column)
        if self.selected_piece and piece == 0 and (row, column) in self.valid_moves:
            self.board.move(self.selected_piece, row, column)
            skipped = self.valid_moves[(row, column)]
            if skipped:
                self.board.remove(skipped)
            self.changeTurn()
        else:
            return False
        return True

    def drawValidMoves(self, moves):
        """Method to draw circles for each of the valid moves"""
        for move in moves:
            row, column = move
            pygame.draw.circle(self.window, BLUE, (column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def changeTurn(self):
        """Method to change player turn"""
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    ######################### AI Methods #########################
    def get_board(self):
        """Method to return the game board"""
        return self.board

    def ai_move(self, board):
        """AI makes move and returns the new board after it has made its move"""
        self.board = board
        self.changeTurn()
    ######################### AI Methods #########################
