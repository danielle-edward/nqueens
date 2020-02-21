#CISC352 nqueens assignment 1
import random
import os

queensOnBoard = []

class Queen:
    def __init__(self, inputCoords):
        self.coords = inputCoords
        self.conflict = False

    def setConflict(self, inputBool):
        self.conflict = inputBool

    def setCoords(self, inputCoords):
        self.coords = inputCoords

def calculateConflicts(curCoords): # this menthod calculates and returns the number of conflicts for a given Queen on the board
    x = curCoords[0]
    y = curCoords[1]
    conflictCount = 0

    for i in queensOnBoard:

        if not ((i.coords[0] == x) and (i.coords[1] == y)):
            if (i.coords[1] == y) or\
               (i.coords[0] - i.coords[1]) == (x - y) or  \
               (i.coords[0] + i.coords[1]) == (x + y):
                    conflictCount = conflictCount + 1

    return conflictCount

def generateBoard(n): # this method will generate an nxn board of n queens. It does so using a "greedy" alogorithm
    global queensOnBoard
    queensOnBoard = []

    curRow = 1

    for i in range(n): # for loop to iterate through each row
        lowestConflict = float('inf')
        for j in range (n): # for loop to iterate through each col to determine where to place the queen on the row
            curColumn = j + 1
            curConflict = calculateConflicts((curRow, curColumn)) # calculate the conflicts that will result from placing a queen at the current spot
            if curConflict < lowestConflict : # if it is the lowest found conflict in the row, that column is the current best column
                bestColumn = curColumn
                lowestConflict = curConflict
            elif curConflict == lowestConflict: # if it is the same as the lowest conflict, then randomly choose the previous best or the current
                rand = random.randint(1,51)
                if(rand < 25):
                    bestColumn = curColumn
                    lowestConflict = curConflict
        tempQueen = Queen((curRow, bestColumn)) # create a Queen with the newly found best coordinates
        queensOnBoard.append(tempQueen) # add that Queen to the queensOnBoard list
        del tempQueen
        curRow = curRow + 1 # move on to next row to find optimal place to put Queen on that row

    for i in queensOnBoard: # for loop to iterate through the origial Queens in the list
        if calculateConflicts(i.coords) > 0: # if that Queens has any conflicts, set its Bool go True
            i.setConflict(True)
        else:                                # else set it to False
            i.setConflict(False)

def solveBoard():
    global queensOnBoard
    n = len(queensOnBoard)
    moves = 0

    while(not all(i.conflict is False for i in queensOnBoard)): # while there are still Queens with conflicts
        randQueen = random.randint(1, n-1)
        curQueen = queensOnBoard[randQueen] # choose a random Queen on the board
        currentConflict = calculateConflicts(queensOnBoard[randQueen].coords) # calculate the conflict of that Queen

        # this helps to avoid getting stuck on local optimum
        if moves == 60: # resets when number of moves hits 60 because it typicall takes less than 50 moves to complete any n queens problem
            queensOnBoard = []
            generateBoard(n)
            moves = 0

        if queensOnBoard[randQueen].conflict is True: # if the randomly chosen Queen has a conflict
            for y in range(n): # iterate through all the columns
                column = y + 1

                if column != queensOnBoard[randQueen].coords[1]: # if we are not on the same column as the random Queen
                    tempConflict = calculateConflicts((queensOnBoard[randQueen].coords[0], column)) # calculate the potential conflicts if the Queen moves to this col
                    if tempConflict < currentConflict: # if the number of potential conflicts is less than the currnet conflicts, move the Queen to that position
                        queensOnBoard[randQueen].setCoords((curQueen.coords[0], column))
                        currentConflict = tempConflict
                        if currentConflict == 0: # if this new position has no conflicts, set that Queen's boolean to False
                            queensOnBoard[randQueen].setConflict(False)

                    elif tempConflict == currentConflict: # if the number of potential conflicts is the same as the current conflicts, randonly choose the new or old position
                        rand2 = random.randint(1,51)
                        if(rand2 < 25):
                            queensOnBoard[randQueen].setCoords((curQueen.coords[0], column))
                            currentConflict = tempConflict
                            if currentConflict == 0: # if this new position has no conflicts, set that Queen's boolean to False
                                queensOnBoard[randQueen].setConflict(False)

            moves = moves + 1 # a move is taken everytime the chosen Queen has conflicts and it goes through each potential column for that Queen

    queensOnBoard.sort(key=lambda x: x.coords[0], reverse=False) # sort the Queens in the list by their x coordinates
    matrix = []
    for i in queensOnBoard: # creates a list of the y coordinates of the Queens. The first index is row 1, the last is row n
        matrix.append(i.coords[1])

    return matrix


def main():
    cwd = os.getcwd().replace('\\', '/') # gets the current working directory of this python file

    f1 = open(cwd + "/nqueens.txt", mode='r') # opens the nqueens file to read the n's from

    f2 = open(cwd + "/nqueens_out.txt", mode='w+') # creates an output file for the matrices to be placed in

    for n in f1:
        print(n)
        generateBoard(int(n)) # a board is generated for each n in the input file
        f2.write("%s\n" % str(solveBoard())) # writes the solution to each size n to the output file

    f2.close()

main()
