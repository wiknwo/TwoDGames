from copy import deepcopy
import pygame
from pycheckers import constants

def minimax(current_board, depth, max_player, game):
    """
    Implementation of minimax algorithm

    Params:
        current_board: The current board for the game
        depth: How far should we extend the decision tree
        max_player: Boolean indicating whether we are the max or min player
        game: The game object being passed to the algorithm
    """
    if depth == 0 or current_board.declareWinner() != None:
        return current_board.evaluate(), current_board
    elif max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(current_board, constants.WHITE, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(current_board, constants.RED, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move

def simulate_move(piece, move, board, game, skip):
    """Function to simulate move on board and return new board after simulating move"""
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board

def get_all_moves(current_board, color, game):
    """Function that returns all possible moves that can be made in a turn"""
    moves = [] # [[board, piece]] make this move then board will look like this
    for piece in current_board.get_all_pieces(color):
        valid_moves = current_board.getValidMoves(piece)
        for move, skip in valid_moves.items():
            # move = (row, column), skip = [pieces to skip]
            tmp_board = deepcopy(current_board)
            tmp_piece = tmp_board.getPiece(piece.row, piece.column)
            new_board = simulate_move(tmp_piece, move, tmp_board, game, skip)
            moves.append(new_board)
    return moves