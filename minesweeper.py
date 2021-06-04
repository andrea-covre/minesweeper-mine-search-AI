'''
    This is the game engine where AIs and Boards are instantiated and executed

    @authors Andrea Covre
    @version 1.2
'''

import time
import os
import sys

from Board import Board
from AI_0 import AI0
from AI_1 import AI1

def main():

    if len(sys.argv) > 2 or len(sys.argv) < 2:
        usage()
    if len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        usage()
    
    file_name = sys.argv[1].split(".")
    if file_name[len(file_name)-1] != "json":
        print("Error: the file must have a JSON extension (.json)")
        exit()

    test = sys.argv[1]

    AI0_total_accesses = 0
    AI0_total_time = 0

    AI1_total_accesses = 0
    AI1_total_time = 0

    counter = 0.0

    test_name = test.split("/")
    test_name = test_name[len(test_name) - 1]

    board = Board(test, 0)
    board_size = board.cols * board.rows

    print("\nTest:")
    print("   Test name:        " + test_name)
    print("   Board dimensions: " + str(board.rows) + "x" + str(board.cols))
    print("   Board area:       " + str(board.rows * board.cols))
    print("   Bombs number:     " + str(board.numBombs))
    print("   Bombs density:    " + str(board.numBombs / (board.rows * board.cols) * 100) + "%")

    start_time = time.time()
    ai0 = AI0(board)
    ai0.playGame()
    end_time = time.time()
    AI0_total_accesses = board.accesses
    AI0_total_time = end_time - start_time

    board = Board(test, 1)
    start_time = time.time()
    ai1 = AI1(board.cols, board.rows, board.numBombs, board.safe)
    bombsLocataion = AI_1_playGame(ai1, board)
    end_time = time.time()
    AI1_total_accesses = board.accesses
    AI1_total_time = end_time - start_time

    print("\nAI-0:")
    print("   Accesses:         " + str(AI0_total_accesses))
    print("   Percentage mined: " + str(round(AI0_total_accesses/board_size * 100, 2)) + "%")
    print("   Time:             " + str(round(AI0_total_time, 4)) + "s")
    printBombList(sorted(ai0.bombsLocation, key=lambda x: (x[0], x[1]))) 

    print("AI-1:")
    print("   Accesses:         " + str(AI1_total_accesses))
    print("   Percentage mined: " + str(round(AI1_total_accesses/board_size * 100, 2)) + "%")
    print("   Time:             " + str(round(AI1_total_time, 4)) + "s")
    printBombList(bombsLocataion)

    print()


def printBoard(board):
    for row in board:
        print(row)


def printBombList(bomb_list):
    LOCATIONS_PER_ROW = 10
    count = 0
    first = True
    for i in range(len(bomb_list)):
        if count == 0 and not first:
            print("                     ", end="")
        if first:
            print("\n   Bombs location:   ", end="")
            first = not first
        
        print("(" + str(bomb_list[i][0]) + ", " + str(bomb_list[i][1]) + ")", end="")
        if i < len(bomb_list) - 1:
            print(", ", end="")

        count = count + 1
        if count >= LOCATIONS_PER_ROW:
            count = 0
            print()
    print()



def AI_1_playGame(ai1, board):
    while len(ai1.bombsFoundSoFar) < board.numBombs:
            next_to_open = ai1.performAI(board.boardState)
            if (next_to_open[0] == 'open_square'):
                board.mine_AI1(next_to_open[1][0], next_to_open[1][1])

            else:
                return sorted(next_to_open[1], key=lambda x: (x[0], x[1]))


def usage():
        print("To run the file use:")
        print("\tminesweeper.py <JSON Board File>")
        sys.exit(1)


if __name__ == "__main__":
    main()