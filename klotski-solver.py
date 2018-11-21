#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import argparse
from klotskigame import KlotskiBoard

if __name__ == "__main__":
    # parse args for number of primes to run
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="File name to open")
    args = parser.parse_args()
    filename = args.filename
    # TODO: abstract file reader
    with open(filename) as file:
        board = []
        lines = 0
        for line in file:
            line = line.strip()
            for x in line:
                board.append(x)
        if len(board) != 20:
            raise Exception("Wrong board size")
        klotskiBoard = KlotskiBoard()
        klotskiBoard.parse_board(board)
        klotskiBoard.find_solution()
        solution = klotskiBoard.get_solution()
        print("Steps are:")
        for p in solution:
            print(p)
            print('\/')
        print('SOLVED')
        print("Number of steps {}".format(len(solution)))
