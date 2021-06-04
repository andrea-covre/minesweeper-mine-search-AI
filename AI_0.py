'''
    This is the AI-0 class that finds the bomb based on a risk score, knowledge gain 
    and minimized probing overlap

    @authors Andrea Covre
    @version 1.8
'''

import json
import copy
import random

class AI0:

    def __init__(self, board):
        self.board = board
        self.rows = board.rows
        self.cols = board.cols
        self.safe = board.safe
        self.numBombs = board.numBombs

        self.maxValue = 8

        self.knowledge = []
        self.untaintedKnowledge = []
        self.riskKnowledgeGain = []
        self.explorativeKnowledgeGain = []

        self.gridOrder = []
        self.nextGridOrderOptions = []
        self.nextRiskOptions = []
        self.nextMove = [self.safe[1], self.safe[0]]

        self.bombsHit = 0
        self.bombsLocation = []
        self.isActive = True
        
        self.generateGridOrder()

        for i in range(self.rows):
            row = []
            rowExpGain = []
            rowUntainted = []
            for j in range(self.cols):
                if (j == self.safe[0] and i == self.safe[1]):
                    row.append([0, "S"])
                    rowUntainted.append(0)
                else:
                    row.append([0, "U"])

                rowUntainted.append(0)
                rowExpGain.append(0)

            self.untaintedKnowledge.append(rowUntainted)
            self.knowledge.append(row)
            self.explorativeKnowledgeGain.append(rowExpGain)
                
 
    '''
        This function generates a list of cells that orderly spaced on the grid 
        as to decrease the number of isolated unmined squares 
    '''

    def generateGridOrder(self):
        for i in range(1, self.rows, 3):
            for j in range(1, self.cols, 3):
                if (i < self.rows and j < self.cols):
                    self.gridOrder.append([i, j])


    '''
        Function called whenever a new square is mined that integrates the new knowledge given by the board
        after mining a square, start the procedures needed to update all the knowledge maps and compute the next move.
        @param {int} x       coordinate of the square mined
        @param {int} y       coordinate of the square mined
        @param {int} mined   value of the mined square
     '''

    def update(self, x, y, mined):
        if (mined == 9):
            mined = "X"
            self.bombsLocation.append([y, x])
            self.knowledge[y][x][0] = 9
            self.knowledge[y][x][1] = "X"
            self.bombsHit = 1 + self.bombsHit

        else:
            self.untaintedKnowledge[y][x] = mined
            self.knowledge[y][x][0] = mined
            self.knowledge[y][x][1] = "M"
        
        self.updateProcedure()



    '''
         Execute the update steps needed
         The update routine is:
                      - offset the mined values           -> offsetMinedValues()
                      - update knowledge                  -> updateKnowledge()
                      - update knowledge gain maps        -> updateKnowledgeGain()
                      - compute the next move             -> getNextMove()
    '''

    def updateProcedure(self):
        self.offsetMinedValues()
        self.updateKnowledge()
        self.updateKnowledgeGain()
        self.getNextMove()
    


    '''
        Offest mined squares based on the mines already identified
    '''

    def offsetMinedValues(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if (self.knowledge[i][j][1] == "M"):
                    i_T = None
                    j_T = None

                    self.knowledge[i][j][0] = self.untaintedKnowledge[i][j]

                    #Loop for a 3x3 moving kernel
                    for k in range(-1, 2):
                        for w in range(-1, 2):
                            i_T = i + k
                            j_T = j + w

                            #Guarding the boundaries, don't compute the kernel cells that are outside the board
                            if (i_T >= 0 and i_T < self.rows and j_T >= 0 and j_T < self.cols):

                                #If the current square was mined and the square we are checking is a bomb, then decrease
                                #the mined value of the current square
                                if (self.knowledge[i_T][j_T][1] == "X" or self.knowledge[i_T][j_T][1] == "H"):
                                    self.knowledge[i][j][0] = - 1 + self.knowledge[i][j][0]


    '''
         Update the knowledge maps related to the square flags and risk scores
    '''

    def updateKnowledge(self):
        newKnowledge = copy.deepcopy(self.knowledge)
        for i in range(self.rows):
            for j in range(self.cols):
                if  (self.knowledge[i][j][1] != "M"):

                    i_T = None
                    j_T = None

                    if  self.knowledge[i][j][1] == "U":
                        newKnowledge[i][j][0] = 0


                    for k in range(-1, 2):
                        for w in range(-1, 2):
                            i_T = i + k
                            j_T = j + w

                            if (i_T >= 0 and i_T < self.rows and j_T >= 0 and j_T < self.cols):

                                #If the this nearby square is == 0, then the current square is safe and flag it with 'S'
                                if (self.knowledge[i_T][j_T][1] == "M"):
                                    if (self.knowledge[i_T][j_T][0] == 0 and newKnowledge[i][j][1] == "U"):
                                        newKnowledge[i][j][1] = "S"

                                #Increase the risk score of the current square based on the mined value of this nearby square 
                                if (self.knowledge[i_T][j_T][0] != 0 and newKnowledge[i][j][1] == "U" and self.knowledge[i_T][j_T][1] == "M"):
                                    newKnowledge[i][j][0] = self.knowledge[i_T][j_T][0] + newKnowledge[i][j][0]

        self.knowledge = copy.deepcopy(newKnowledge)


    '''
         This function follows the same procedures as update(), but updates the knowledge gain map
         which can only be updated once the knowledge map has been updated from the lates mining 
    '''
    
    def updateKnowledgeGain(self):

        #Reset the arrays of next moves
        self.nextRiskOptions = []

        for i in range(self.rows):
            for j in range(self.cols):

                self.explorativeKnowledgeGain[i][j] = 0

                if  (self.knowledge[i][j][1] != "M"):

                    i_T = None
                    j_T = None

                    for k in range(-1, 2):
                        for w in range(-1, 2):
                            i_T = i + k
                            j_T = j + w

                            if (i_T >= 0 and i_T < self.rows and j_T >= 0 and j_T < self.cols):

                                #Increase explorative knowledge gain based on how many non-mined squares are around
                                if (self.knowledge[i_T][j_T][1] == "U"):
                                    self.explorativeKnowledgeGain[i][j] = 1 + self.explorativeKnowledgeGain[i][j]



                #Consider only the unsafe squares
                if (self.knowledge[i][j][1] == "U"):

                    #If no option yet, then add the current square to the list
                    if (len(self.nextRiskOptions) == 0):
                        self.nextRiskOptions = [[i, j]]

                    else:

                        
                        #If the current square has the highest risk knowledge gain so far then make it the new record
                        if (self.knowledge[i][j][0] > self.knowledge[self.nextRiskOptions[0][0]][self.nextRiskOptions[0][1]][0]):
                            self.nextRiskOptions = [[i, j]]

                        #If the current square has the same record high risk then check explorative knowledge gain
                        elif (self.knowledge[i][j][0] == self.knowledge[self.nextRiskOptions[0][0]][self.nextRiskOptions[0][1]][0]):

                            #If the current square has the highest explorative knowledge gain then make it the new record
                            if (self.explorativeKnowledgeGain[i][j] > self.explorativeKnowledgeGain[self.nextRiskOptions[0][0]][self.nextRiskOptions[0][1]]):
                                self.nextRiskOptions = [[i, j]]

                            #If the current square has the same record high risk and explorative knowledge gain then add it to the other records
                            elif (self.explorativeKnowledgeGain[i][j] == self.explorativeKnowledgeGain[self.nextRiskOptions[0][0]][self.nextRiskOptions[0][1]]):
                                self.nextRiskOptions.append([i, j])
 



    '''
         Gets the next move prioritizing risk, and then explorative gain
    '''

    def getNextMove(self):

        #if all bombs have been found or if there is not other smart move then close the game
        if (self.bombsHit == self.numBombs or len(self.nextRiskOptions) == 0):
            self.isActive = False
            return

        #updating the next best grid order option including all the grid order options with max explorative gain 
        self.nextGridOrderOptions = []
        for square in self.gridOrder:
            if (self.explorativeKnowledgeGain[square[0]][square[1]] == 9):
                self.nextGridOrderOptions.append(square)

        self.nextGridOrderOptions = [];  #uncomment to deactivate nextGridOrder

        #If there is no next risk option available with positve risk then pick an option from the grid order
        if (self.knowledge[self.nextRiskOptions[0][0]][self.nextRiskOptions[0][1]][0] == 0 and len(self.nextGridOrderOptions) != 0):
        
            #this.nextMove = this.nextUnsafeOptions[Math.floor(Math.random() * this.nextUnsafeOptions.length)];
            self.nextMove = self.nextGridOrderOptions[0]

        #Otherwise pick randomly one of the highest risk score squares (and then highest explorative gain)
        else:
            self.nextMove = self.nextRiskOptions[random.randrange(0, len(self.nextRiskOptions))]


    '''
        Play the next move 
    '''

    def playNext(self):
        self.update(self.nextMove[1], self.nextMove[0], self.board.mine(self.nextMove[1], self.nextMove[0]))


    '''
        Play the whole game
    '''

    def playGame(self):
        while(self.isActive):
            self.playNext()
        #print("%d/%d  bombs found" % (self.bombsHit, self.numBombs))

