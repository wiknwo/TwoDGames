import pygame
from .constants import RED, SQUARE_SIZE, WHITE, GREY, CROWN

class Piece:
    """
    An uncrowned piece (man) moves one step diagonally 
    forwards and captures an adjacent opponent's piece by 
    jumping over it and landing on the next square. 
    Multiple enemy pieces can be captured in a single turn 
    provided this is done by successive jumps made by a 
    single piece; the jumps do not need to be in the same 
    line and may "zigzag" (change diagonal direction). In 
    American checkers, men can jump only forwards; in 
    international draughts and Russian draughts, men can 
    jump both forwards and backwards.
    """
    PADDING = 10
    OUTLINE = 2

    def __init__(self, row, column, color):
        """Method to initialize variables for Piece object"""
        self.row = row
        self.column = column
        self.color = color
        self.isKing = False
        self.x = 0
        self.y = 0

    def calculatePosition(self):
        """Calculate te position of this piece based on the row and column it is in"""
        self.x = SQUARE_SIZE * self.column + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
    
    def makeKing(self):
        """
        Promote this piece to a king. When a man reaches 
        the farthest row forward, known as the kings row or 
        crownhead, it becomes a king. It is marked by 
        placing an additional piece on top of, or crowning, 
        the first man. The king has additional powers, 
        including the ability to move backwards and, in 
        variants where men cannot already do so, capture 
        backwards. Like a man, a king can make successive 
        jumps in a single turn, provided that each jump 
        captures an enemy piece.

        In international draughts, kings (also called 
        flying kings) move any distance along unblocked 
        diagonals. They may capture an opposing man any d
        istance away by jumping to any of the unoccupied 
        squares immediately beyond it. Because jumped 
        pieces remain on the board until the turn is 
        complete, it is possible to reach a position in a 
        multi-jump move where the flying king is blocked 
        from capturing further by a piece already jumped.

        Flying kings are not used in American checkers; a 
        king's only advantage over a man is the additional 
        ability to move and capture backwards.
        """
        self.isKing = True
    
    def draw(self, window):
        """Method to draw this piece"""
        self.calculatePosition() # https://stackoverflow.com/questions/65309004/plotting-pieces-on-a-checkerboard-using-pygame
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(window, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        if self.isKing:
            window.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))
        
    def move(self, row, column):
        """Method to move piece to new position"""
        self.row = row
        self.column = column
        self.calculatePosition()

    def __repr__(self):
        """Method to return string representation of piece object"""
        return str(self.color)