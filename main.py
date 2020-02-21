#CISC352 nqueens assignment 1
import random


#So this implementation works, problem is I haven't decided on a criteria to decide
#when it has gotten stuck on local hill, any suggestions would be great lmao



queensOnBoard = []


class Queen:
    def __init__(self, inputCoords):
        self.coords = inputCoords
        self.conflict = False

    def setConflict(self, inputBool):
        self.conflict = inputBool

    def setCoords(self, inputCoords):
        self.coords = inputCoords


def calculateConflictsQueen(curQueen):
    x = curQueen.coords[0]
    y = curQueen.coords[1]
    conflictCount = 0

    for i in queensOnBoard:
        
        if i != curQueen: 
            if(i.coords[0] == x) or (i.coords[1] == y) or\
               (i.coords[0] - i.coords[1]) == (x - y) or  \
               (i.coords[0] + i.coords[1]) == (x + y):
                    conflictCount = conflictCount + 1
            
    return conflictCount



def calculateConflicts(curCoords):
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
        
    

def generateBoard(n):
    curRow = 1
    
    for i in range(n):
        lowestConflict = float('inf')
        for j in range (n):
            curColumn = j + 1
            curConflict = calculateConflicts((curRow, curColumn))
            if curConflict < lowestConflict :
                bestColumn = curColumn
                lowestConflict = curConflict
            elif curConflict == lowestConflict:
                rand = random.randint(1,51)
                if(rand < 25):
                    bestColumn = curColumn
                    lowestConflict = curConflict
        tempQueen = Queen((curRow, bestColumn))
        queensOnBoard.append(tempQueen)
        del tempQueen
        curRow = curRow + 1

    for i in queensOnBoard:
        if calculateConflicts(i.coords) > 0:
            i.setConflict(True)
        else:
            i.setConflict(False)



def solveBoard():
    global queensOnBoard
    n = len(queensOnBoard)
    moves = 0

   
        
    
    while(not all(i.conflict is False for i in queensOnBoard)):
        randQueen = random.randint(1, n-1)
        curQueen = queensOnBoard[randQueen]
        currentConflict = calculateConflicts(queensOnBoard[randQueen].coords)

        if moves == 60:
            queensOnBoard = []
            generateBoard(n)
            moves = 0
            print("reset")


        
        if queensOnBoard[randQueen].conflict is True:
            for y in range(n):
                column = y + 1
                
                if column != queensOnBoard[randQueen].coords[1]:
                    tempConflict = calculateConflicts((queensOnBoard[randQueen].coords[0], column))
                    if tempConflict < currentConflict:
                        queensOnBoard[randQueen].setCoords((curQueen.coords[0], column))
                        currentConflict = tempConflict
                        if currentConflict == 0:
                            queensOnBoard[randQueen].setConflict(False)
                            
                    elif tempConflict < currentConflict:
                        rand2 = random.randint(1,51)
                        if(rand < 25):
                            queensOnBoard[randQueen].setCoords((curQueen.coords[0], column))
                            currentConflict = tempConflict
                            if currentConflict == 0:
                                queensOnBoard[randQueen].setConflict(False)
 
            moves = moves + 1
          
    queensOnBoard.sort(key=lambda x: x.coords[0], reverse=False)
    matrix = []
    for i in queensOnBoard:
        matrix.append(i.coords[1])

    return matrix


def main():
    #Q1 = Queen((1,4))
    #Q2 = Queen((2,2))
    #Q3 = Queen((3,7))
    #Q4 = Queen((4,3))
    #Q5 = Queen((5,6))
    #Q6 = Queen((6,8))
    #Q7 = Queen((7,5))
    #Q8 = Queen((8,3))
    #Q8.setConflict(True)

    #queensOnBoard.append(Q1)
    #queensOnBoard.append(Q2)
    #queensOnBoard.append(Q3)
    #queensOnBoard.append(Q4)
    #queensOnBoard.append(Q5)
    #queensOnBoard.append(Q6)
    #queensOnBoard.append(Q7)
    #queensOnBoard.append(Q8)

 
 

    #print("Should be 0: " + str(calculateConflicts(Q1.coords)))
    #print("Should be 1: " + str(calculateConflicts(Q2)))
    #print("Should be 0: " + str(calculateConflicts(Q3.coords)))
    #print("Should be 2: " + str(calculateConflicts(Q4)))

    generateBoard(8)

    #for i in queensOnBoard:
        #print(str(i.coords) + " is conflicting: " + str(i.conflict))
    answer = solveBoard()
    print(answer)

main()

    
