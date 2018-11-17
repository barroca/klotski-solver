# -*- encoding: utf-8 -*-
from .exceptions import WrongPieceValue, PieceAlreadyInPlace, ProblematicPiece, MissingPiece

BOARD_COLUMN_SIZE = 4
BOARD_LINE_SIZE = 5

class KlotskBoard():
    def __init__(self, board):
        self.board = self.boardParser(board)

    def boardParser(self, board):
        # possible have the values that we can have on our board array
        # a-j represents pieces
        # '0' represents already checked spot
        # ' ' represents empty space
        possible = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', ' ', '0']
        found = {}
        board_ok = ['0'] * BOARD_COLUMN_SIZE * BOARD_LINE_SIZE
        for i in range(BOARD_COLUMN_SIZE * BOARD_LINE_SIZE):
            x = board[i]
            if x not in possible:
                raise WrongPieceValue(x)
            if x in found:
                raise PieceAlreadyInPlace(x)
            if x == 'a' or x == 'c' or x == 'd' or x == 'f':
                # we are with vertical Piece
                # we check if the botton value is the same.
                if i+4 < BOARD_COLUMN_SIZE * BOARD_LINE_SIZE and board[i+BOARD_COLUMN_SIZE] == x:
                    board_ok[i] = x
                    board[i] = '0'
                    board_ok[i+BOARD_COLUMN_SIZE] = x
                    board[i+BOARD_COLUMN_SIZE] = '0'
                    found[x] = True
                else:
                    raise ProblematicPiece(x)
            if x == 'e':
                # we are with horizontal Piece
                # we check if next value is the same and is in the same line
                if board[i+1] == x and (i+1 % BOARD_COLUMN_SIZE+1) != 0:
                    board_ok[i] = x
                    board_ok[i+1] = x
                    board[i] = '0'
                    board[i+1] = '0'
                    found[x] = True
                else:
                    raise ProblematicPiece(x)
            if x == 'g' or x == 'h' or x == 'i' or x == 'j':
                # we are with dot piece, don't need to check neighbors
                board_ok[i] = x
                board[i] = '0'
                found[x] = True
            if x == 'b':
                # this is the square piece
                # need to check both next neighbor and line below.
                if i+4 < BOARD_COLUMN_SIZE * BOARD_LINE_SIZE and board[i+BOARD_COLUMN_SIZE] == x and board[i+1] == x and \
                   (i+1 % BOARD_COLUMN_SIZE+1) != 0 and i+BOARD_COLUMN_SIZE+1 < BOARD_COLUMN_SIZE * BOARD_LINE_SIZE and board[i+BOARD_COLUMN_SIZE+1] == x:
                    board_ok[i] = x
                    board_ok[i+1] = x
                    board_ok[i+BOARD_COLUMN_SIZE] = x
                    board_ok[i+BOARD_COLUMN_SIZE+1] = x
                    board[i] = '0'
                    board[i+1] = '0'
                    board[i+BOARD_COLUMN_SIZE] = '0'
                    board[i+BOARD_COLUMN_SIZE+1] = '0'
                    found[x] = True
                else:
                    raise ProblematicPiece(x)
        if len(found) != 10:
            raise MissingPiece(found.keys())
        return board_ok

    def boardHash(self):
        return ''.join(self.board)
