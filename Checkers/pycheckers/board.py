import pygame
from .constants import BLACK, ROWS, COLUMNS, RED, SQUARE_SIZE, WHITE # .constants because when we are in same directory as something else, we are specifying that we are making a relative import
from .piece import Piece

class Board:
    """Class representing Checkers board of size 8x8"""
    def __init__(self):
        """Method to initialize board variables"""
        self.board = []
        self.red_pieces_remaining = self.white_pieces_remaining = 12
        self.red_kings = self.white_kings = 0
        self.createBoard()
    
    def drawCheckerboardPattern(self, window):
        """Method to draw squares in chequered pattern on board"""
        window.fill(BLACK)
        for row_index in range(ROWS):
            for column_index in range(row_index % 2, COLUMNS, 2):
                pygame.draw.rect(window, RED, (row_index * SQUARE_SIZE, column_index * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, column):
        """Method to move piece by deleting piece from where it is and changing its position"""
        self.board[piece.row][piece.column], self.board[row][column] = self.board[row][column], self.board[piece.row][piece.column]
        piece.move(row, column)
        # Checking if we move into first or last row to see if piece should become king
        if row == ROWS - 1 or row == 0:
            piece.makeKing()
            if piece.color == WHITE:
                self.white_kings += 1
            elif piece.color == RED:
                self.red_kings += 1
    
    def getPiece(self, row, column):
        """Method to get piece on board"""
        return self.board[row][column]

    def createBoard(self):
        """Method to create pieces with white at top and red at bottom"""
        for row_index in range(ROWS):
            self.board.append([]) # Want interior lists for each row
            for column_index in range(COLUMNS):
                if column_index % 2 == ((row_index + 1) % 2):
                    if row_index < 3:
                        self.board[row_index].append(Piece(row_index, column_index, WHITE))
                    elif row_index > 4:
                        self.board[row_index].append(Piece(row_index, column_index, RED))
                    else:
                        self.board[row_index].append(0) # Blank piece
                else:
                    self.board[row_index].append(0)

    def draw(self, window):
        """Method to draw pieces and squares"""
        self.drawCheckerboardPattern(window)
        for row_index in range(ROWS):
            for column_index in range(COLUMNS):
                piece = self.board[row_index][column_index]
                if piece != 0:
                    piece.draw(window)

    def remove(self, pieces):
        """Method to remove all specified pieces from board"""
        for piece in pieces:
            self.board[piece.row][piece.column] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_pieces_remaining -= 1
                else:
                    self.white_pieces_remaining -= 1

    def declareWinner(self):
        """Method to determine who won the checkers game"""
        if self.red_pieces_remaining <= 0:
            return WHITE
        elif self.white_pieces_remaining <= 0:
            return RED
        return None
    
    def getValidMoves(self, piece):
        """Method to perform part of algorithm that determines valid moves for piece"""
        # Red pieces are at the bottom so direction they are moving is negative with respect to pygame coordinate system
        # White pieces are at the top so direction they are moving is positive with respect to pygame coordinate system
        moves = {} # key: (row, column), value: []
        left = piece.column - 1
        right = piece.column + 1
        row = piece.row
        if piece.color == RED or piece.isKing:
            moves.update(self.__traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self.__traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.isKing:
            moves.update(self.__traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self.__traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        return moves

    def __traverse_left(self, start, stop, step, color, left, skipped = []):
        """Private method that implements part of the algorithm to determine valid moves of a piece"""
        moves = {}
        last = [] # Piece we would skip to move to where we want to go
        for row_index in range(start, stop, step):
            if left < 0:
                break
            current = self.board[row_index][left]
            if current == 0: # We found a blank square
                row = 8 # Initialize row using 8 as sentinel
                if skipped and not last: # We skipped over something, we found a blank square and we don't have anything we can skip again then we can't move there
                    break
                elif skipped:
                    moves[(row_index, left)] = last + skipped # Double jumping
                else:
                    moves[(row_index, left)] = last
                if last:
                    if step == -1:
                        row = max(row_index - 3, 0)
                    else:
                        row = min(row_index + 3, ROWS)
                moves.update(self.__traverse_left(row_index + step, row, step, color, left - 1, skipped = last))
                moves.update(self.__traverse_right(row_index + step, row, step, color, left + 1, skipped = last))
                break            
            elif current.color == color: # Piece we are trying to move to is same color as our piece then we can't move
                break
            else: # Piece is not our color so we could potentially jump over it if there is a blank square adjacent to it
                last = [current]
            left -= 1
        return moves

    def __traverse_right(self, start, stop, step, color, right, skipped = []):
        """Private method that implements part of the algorithm to determine valid moves of a piece"""
        moves = {}
        last = [] # Piece we would skip to move to where we want to go
        for row_index in range(start, stop, step):
            if right >= COLUMNS:
                break
            current = self.board[row_index][right]
            if current == 0: # We found a blank square
                row = 8 # Initialize row using 8 as sentinel
                if skipped and not last: # We skipped over something, we found a blank square and we don't have anything we can skip again then we can't move there
                    break
                elif skipped:
                    moves[(row_index, right)] = last + skipped # Double jumping
                else:
                    moves[(row_index, right)] = last
                if last:
                    if step == -1:
                        row = max(row_index - 3, 0)
                    else:
                        row = min(row_index + 3, ROWS)
                moves.update(self.__traverse_left(row_index + step, row, step, color, right - 1, skipped = last))
                moves.update(self.__traverse_right(row_index + step, row, step, color, right + 1, skipped = last))
                break            
            elif current.color == color: # Piece we are trying to move to is same color as our piece then we can't move
                break
            else: # Piece is not our color so we could potentially jump over it if there is a blank square adjacent to it
                last = [current]
            right += 1
        return moves