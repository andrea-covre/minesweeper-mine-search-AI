'''
    This is the board class that takes in a JSON file, parses it, stores all the related information 
    about the board that is being played, manages the mining and counts the accesses

    @authors Andrea Covre
    @version 1.3
'''

import json

class Board:

    def __init__(self, fileName, ai_type):
        try:
            fileData = open(fileName, "r")
        except:
            print("Error: " + fileName + " could not be found")
            exit()

        try:
            self.data = json.load(fileData)
            fileData.close()
            self.rows = int(self.data["dim"].split(",")[0])
            self.cols = int(self.data["dim"].split(",")[1])
            self.safe = [int(self.data["safe"].split(",")[1]), int(self.data["safe"].split(",")[0])]
            self.numBombs = int(self.data["bombs"])
            self.board = []
            self.boardState = []
            self.accesses = 0
        except:
            print("Error: " + fileName + " is not a compatible format")
            exit()

        if ai_type == 0:
            for i in range(self.rows):
                row = []
                for j in range(self.cols):
                    row.append(int(self.data["board"][i * self.cols + j]))
                self.board.append(row)

        else:
            for i in range(self.cols):
                row = []
                rowState = []
                for j in range(self.rows):
                    row.append(int(self.data["board"][i * self.rows + j]))
                    rowState.append(-1)
                self.board.append(row)
                self.boardState.append(rowState)

    
    def mine(self, x, y):
        self.accesses = 1 + self.accesses
        return self.board[y][x]


    def mine_AI1(self, x, y):
        self.accesses = 1 + self.accesses
        self.boardState[x][y] = self.board[x][y]






