'''
    @authors Parisha Reddy
'''

import numpy as np
import random

class AI1():

    # Define settings upon initialization. Here you can specify
    def __init__(self, numRows, numCols, numBombs, safeSquare):

        # game variables that can be accessed in any method in the class. For example, to access the number of rows, use "self.numRows"
        self.numRows = numRows
        self.numCols = numCols
        self.numBombs = numBombs
        self.safeSquare = safeSquare
        self.safeList = []
        self.explore = []
        self.bombsFoundSoFar = []
        self.firstIteration = True

    def open_square_format(self, squareToOpen):
        return ("open_square", squareToOpen)

    def submit_final_answer_format(self, listOfBombs):
        return ("final_answer", listOfBombs)


    def performAI(self, boardState):

        # for row in boardState:
        #     print(row)

        # find all the unopened squares
        if self.firstIteration:
            self.explore.append(self.safeSquare)
            self.firstIteration = False
        if self.explore:
            currOpen = self.explore.pop(0)
            if boardState[currOpen[0]][currOpen[1]] == 9 and currOpen not in self.bombsFoundSoFar:
                self.bombsFoundSoFar.append(currOpen)
                if currOpen in self.explore:
                    self.explore.remove(currOpen)
                if (len(self.bombsFoundSoFar) == self.numBombs):
                    # print(f"List of bombs is {self.bombsFoundSoFar}")
                    return self.submit_final_answer_format(self.bombsFoundSoFar)
            #AFN#
            elif boardState[currOpen[0]][currOpen[1]] == 0:
                for i in range(currOpen[0]-1, currOpen[0]+2):
                    for j in range(currOpen[1]-1, currOpen[1]+2):
                        if i >= 0 and i < self.numRows:
                            if j >= 0 and j < self.numCols:
                                if not (i == currOpen[0] and j == currOpen[1]):
                                    if boardState[i][j] == -1 and (i,j) not in self.safeList:
                                        self.safeList.append((i, j))
            #AMN#
            else:
                ret = self.isAMN(currOpen, boardState)
                if ret:
                    return ret
        for row in range(self.numRows):
            for col in range(self.numCols):
                if boardState[row][col] > 0:
                    ret = self.isAMN((row,col), boardState)
                    if ret:
                        return ret
        if self.explore:
            currOpen = self.explore[0]
            # print(f"Square to open is {currOpen}")
            return self.open_square_format(currOpen)

        unopenedSquares = []
        for row in range(self.numRows):
            for col in range(self.numCols):
                if boardState[row][col] == -1 and (row, col) not in self.safeList:
                    unopenedSquares.append((row, col))
        squareToOpen = random.choice(unopenedSquares)
        self.explore.append(squareToOpen)
        # print(f"Square to open is {squareToOpen}")
        return self.open_square_format(squareToOpen)

    def isAMN(self, currOpen, boardState):
        unopenNeighbors = 0
        bombsNearby = boardState[currOpen[0]][currOpen[1]]
        for i in range(currOpen[0]-1, currOpen[0]+2):
            for j in range(currOpen[1]-1, currOpen[1]+2):
                if i >= 0 and i < self.numRows:
                    if j >= 0 and j < self.numCols:
                        if not (i == currOpen[0] and j == currOpen[1]):
                            if boardState[i][j] == -1:
                                unopenNeighbors = unopenNeighbors + 1
                            if boardState[i][j] == 9:
                                bombsNearby = bombsNearby - 1
        if unopenNeighbors == bombsNearby:
            for i in range(currOpen[0]-1, currOpen[0]+2):
                for j in range(currOpen[1]-1, currOpen[1]+2):
                    if i >= 0 and i < self.numRows:
                        if j >= 0 and j < self.numCols:
                            if not (i == currOpen[0] and j == currOpen[1]):
                                if (boardState[i][j] == -1) and (i, j) not in self.bombsFoundSoFar:
                                    self.bombsFoundSoFar.append((i, j))
                                    if (i, j) in self.explore:
                                        self.explore.remove((i, j))
                                    if (len(self.bombsFoundSoFar) == self.numBombs):
                                        # print(f"List of bombs is {self.bombsFoundSoFar}")
                                        return self.submit_final_answer_format(self.bombsFoundSoFar)
        else:
            for i in range(currOpen[0]-1, currOpen[0]+2):
                for j in range(currOpen[1]-1, currOpen[1]+2):
                    if i >= 0 and i < self.numRows:
                        if j >= 0 and j < self.numCols:
                            if not (i == currOpen[0] and j == currOpen[1]):
                                if (boardState[i][j] == -1) and (i, j) not in self.bombsFoundSoFar:
                                    if (i,j) not in self.safeList and (i,j) not in self.explore:
                                        self.explore.append((i,j))
