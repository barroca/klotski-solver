# -*- encoding: utf-8 -*-
from unittest import TestCase
from klotskigame import KlotskiBoard
from klotskigame.exceptions import WrongPieceValue, PieceAlreadyInPlace,\
    ProblematicPiece, MissingPiece


class KlotskiBoardPlacementTest(TestCase):
    def setUp(self):
        self.values = [x for x in 'abbcabbcdeefdghfi  j']

    ''' This test checks the Exceptions '''
    def test_wrong_piece_value(self):
        with self.assertRaises(WrongPieceValue):
            values = self.values.copy()
            values[0] = 'x'
            board = KlotskiBoard()
            board.parse_board(values)

    def test_problematic_piece(self):
        with self.assertRaises(ProblematicPiece):
            values = self.values.copy()
            values[0] = 'b'
            board = KlotskiBoard()
            board.parse_board(values)

    def test_piece_already_in_place(self):
        with self.assertRaises(PieceAlreadyInPlace):
            values = self.values.copy()
            values[9] = 'a'
            values[10] = 'a'
            board = KlotskiBoard()
            board.parse_board(values)

    def test_missing_piece(self):
        with self.assertRaises(MissingPiece):
            values = self.values.copy()
            values[9] = ' '
            values[10] = ' '
            board = KlotskiBoard()
            board.parse_board(values)
