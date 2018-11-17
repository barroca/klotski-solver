# -*- encoding: utf-8 -*-


class KlotskBoardException(Exception):
    def __init__(self, piece, kind_message):
        message = "Wrong board configuration: {} '{}'".format(kind_message, piece)
        super().__init__(message)


class WrongPieceValue(KlotskBoardException):
    def __init__(self, x):
        super().__init__(x, "wrong piece value")


class PieceAlreadyInPlace(KlotskBoardException):
    def __init__(self, x):
        super().__init__(x, "piece already in place")


class ProblematicPiece(KlotskBoardException):
    def __init__(self, x):
        super().__init__(x, "check piece")


class MissingPiece(KlotskBoardException):
    def __init__(self, x):
        super().__init__(x, "missing piece, current pieces are:")
