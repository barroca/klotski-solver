# -*- encoding: utf-8 -*-
from .exceptions import WrongPieceValue, PieceAlreadyInPlace, \
    ProblematicPiece, MissingPiece
from queue import Queue

# Constants for board size
BOARD_COLUMN_SIZE = 4
BOARD_LINE_SIZE = 5
BOARD_SIZE = BOARD_LINE_SIZE * BOARD_COLUMN_SIZE


class Piece():
    def __init__(self, label, occupied):
        self.label = label
        self.occupied = occupied
        '''
        Directions are:
        0: up
        1: right
        2: down
        3: left
        '''
        self.movement_offsets = [-BOARD_COLUMN_SIZE, 1, BOARD_COLUMN_SIZE, -1]

    # copy in a new object
    def copy(self):
        occupied = list(self.occupied)
        label = self.label
        return Piece(label, occupied)

    # check if piece can move to direction on the board
    def can_move(self, direction, board):
        offset = self.movement_offsets[direction]
        for x in self.occupied:
            new_positon = x + offset
            if new_positon < 0 or new_positon >= BOARD_SIZE:
                return False
            if board[new_positon] != '0' and board[new_positon] != self.label:
                return False
            # we are at the side, can't move left
            if x % BOARD_COLUMN_SIZE == 0 and direction == 3:
                return False
            # we are at the side, can't move left
            if new_positon % BOARD_COLUMN_SIZE == 0 and direction == 1:
                return False
            # we reached the botton, can't move down
            if new_positon >= BOARD_SIZE and direction == 2:
                return False
            # we are at the top, can't move up
            if new_positon < 0 and direction == 0:
                return False
        return True

    # change piece positioning on that direction
    def new_positon_for_piece(self, direction):
        offset = self.movement_offsets[direction]
        new_positon = []
        for x in self.occupied:
            new_positon.append(x + offset)
        return new_positon


class KlotskiBoard():
    def __init__(self):
        self.previous = None
        self.board = ['0'] * BOARD_SIZE
        self.pieces = []
        self.solved = False
        self.solution_path = []

    # copy the content of this object into a new one
    def copy(self):
        board = KlotskiBoard()
        board.board = list(self.board)
        board.pieces = [x.copy() for x in self.pieces]
        return board

    # print into string for presenting the path
    def __str__(self):
        output = ''
        for i in range(BOARD_SIZE):
            if i > 0 and i % BOARD_COLUMN_SIZE == 0:
                output += '\n'
            output += self.board[i] if not i == '0' else ' '
        return output

    # print encoded string to be used on frontend
    def stringfy(self):
        return ''.join(self.board)

    # check if vertical piece fits into board
    def _vertical_piece_placement(self, x, i, board, board_ok):
        if (i+BOARD_COLUMN_SIZE < BOARD_SIZE and
           board[i+BOARD_COLUMN_SIZE] == x):
            occupied = [i, i+BOARD_COLUMN_SIZE]
            board_ok[i] = x
            board[i] = '0'
            board_ok[i+BOARD_COLUMN_SIZE] = x
            board[i+BOARD_COLUMN_SIZE] = '0'
            piece = Piece(x, occupied)
            return piece
        return False

    # check if horizontal piece fits into board
    def _horizontal_piece_placement(self, x, i, board, board_ok):
        if board[i+1] == x and (i+1 % BOARD_COLUMN_SIZE) != 0:
            occupied = [i, i+1]
            board_ok[i] = x
            board_ok[i+1] = x
            board[i] = '0'
            board[i+1] = '0'
            piece = Piece(x, occupied)
            return piece
        return False

    # add small square piece
    def _dot_piece_placement(self, x, i, board, board_ok):
        occupied = [i]
        board_ok[i] = x
        board[i] = '0'
        piece = Piece(x, occupied)
        return piece

    # check if big square can fit
    def _square_piece_placement(self, x, i, board, board_ok):
        if (i+BOARD_COLUMN_SIZE < BOARD_SIZE and
           board[i+BOARD_COLUMN_SIZE] == x and
           board[i+1] == x and
           (i+1 % BOARD_COLUMN_SIZE) != 0 and
           i+BOARD_COLUMN_SIZE+1 < BOARD_SIZE and
           board[i+BOARD_COLUMN_SIZE+1] == x):
            occupied = [i, i+1, i+BOARD_COLUMN_SIZE, i+BOARD_COLUMN_SIZE+1]
            board_ok[i] = x
            board_ok[i+1] = x
            board_ok[i+BOARD_COLUMN_SIZE] = x
            board_ok[i+BOARD_COLUMN_SIZE+1] = x
            board[i] = '0'
            board[i+1] = '0'
            board[i+BOARD_COLUMN_SIZE] = '0'
            board[i+BOARD_COLUMN_SIZE+1] = '0'
            piece = Piece(x, occupied)
            return piece
        return False

    ''' This function parses the initial board and check if is correct
        If the parsed board is wrong it raises exceptions accordingly
    '''
    def parse_board(self, board):
        # possible have the values that we can have on our board array
        # a-j represents pieces
        # '0' represents already checked spot
        # ' ' represents empty space
        possible = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', ' ', '0']
        found = {}
        board_ok = ['0'] * BOARD_SIZE
        for i in range(BOARD_SIZE):
            x = board[i]
            if x not in possible:
                raise WrongPieceValue(x)
            if x in found:
                raise PieceAlreadyInPlace(x)
            if x == 'a' or x == 'c' or x == 'd' or x == 'f':
                # we are with vertical Piece
                # we check if the botton value is the same.
                piece = self._vertical_piece_placement(x, i, board, board_ok)
                if isinstance(piece, Piece):
                    found[x] = True
                    self.pieces.append(piece)
                else:
                    raise ProblematicPiece(x)
            if x == 'e':
                # we are with horizontal Piece
                # we check if next value is the same and is in the same line
                piece = self._horizontal_piece_placement(x, i, board, board_ok)
                if isinstance(piece, Piece):
                    found[x] = True
                    self.pieces.append(piece)
                else:
                    raise ProblematicPiece(x)
            if x == 'g' or x == 'h' or x == 'i' or x == 'j':
                # we are with dot piece, don't need to check neighbors
                piece = self._dot_piece_placement(x, i, board, board_ok)
                found[x] = True
                self.pieces.append(piece)
            if x == 'b':
                # this is the square piece
                # need to check both next neighbor and line below.
                piece = self._square_piece_placement(x, i, board, board_ok)
                if isinstance(piece, Piece):
                    found[x] = True
                    self.pieces.append(piece)
                    found[x] = True
                else:
                    raise ProblematicPiece(x)
        if len(found) != 10:
            raise MissingPiece(found.keys())
        self.board = board_ok

    # create a hash for the state of board
    def board_hash(self):
        # since some elements have the same size, we don't need to produce all
        # combinations of moviments, to avoid this our hash function produces
        # the same hash for different pieces
        hash_translation = {
            'a': 'a',
            'c': 'a',
            'd': 'a',
            'f': 'a',
            'g': 'g',
            'h': 'g',
            'i': 'g',
            'j': 'g',
            'b': 'b',
            'e': 'e',
            ' ': '0',
            '0': '0'
        }
        return ''.join([hash_translation[s] for s in self.board])

    # evaluate if it is a solution
    def is_solution(self):
        return ((self.board[14] == '0' and self.board[17] == 'b' and
                 self.board[18] == '0') or
                (self.board[13] == '0' and self.board[17] == '0' and
                 self.board[18] == 'b') or
                (self.board[13] == 'b' and self.board[14] == 'b' and
                 self.board[17] == '0' and self.board[18] == '0'))

    # function to visit move pieces on board, this uses BFS. For each board
    # configuration (Vertex) we produce every new board based on a
    # movement (Edge).
    def visit(self):
        visited = {}
        q = Queue()
        q.put(self)
        visited[self.board_hash()] = True
        while not q.empty():
            v = q.get()
            next_boards = v.generate_boards()
            for w in next_boards:
                hash = w.board_hash()
                if hash in visited:
                    continue
                w.previous = v
                if w.is_solution():
                    return w
                q.put(w)

                visited[hash] = True

    # move this piece on the board building a new board with
    # this configuration
    def move_this_piece(self, piece, movement):
        new_board = self.copy()
        new_positon = piece.new_positon_for_piece(movement)
        for p in piece.occupied:
            new_board.board[p] = '0'
        for p in new_positon:
            new_board.board[p] = piece.label
        for p in new_board.pieces:
            if p.label == piece.label:
                p.occupied = new_positon
                break
        return new_board

    # generate all possible boards from the current state
    def generate_boards(self):
        boards = []
        for piece in self.pieces:
            for movement in [2, 0, 3, 1]:
                if piece.can_move(movement, self.board):
                    new_board = self.move_this_piece(piece, movement)
                    boards.append(new_board)
                    if piece.can_move(movement, new_board.board):
                        two_steps_board =\
                            new_board.move_this_piece(piece, movement)
                        boards.append(two_steps_board)
        return boards

    # find the solution and store it on this object
    def find_solution(self):
        v = self.visit()
        path = []
        s = v
        while s is not None:
            path.append(s)
            s = s.previous
        path.reverse()
        self.solution_path = path
        self.solved = True
        return True

    # return the solution into desired format
    def get_solution(self, stringfy=False):
        if not self.solved:
            raise Exception('Board not solved yet')
        if stringfy:
            result = []
            for step in self.solution_path:
                result.append(step.stringfy())
            return result
        return self.solution_path
