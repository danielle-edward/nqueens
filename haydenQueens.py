import os
import random
import time
class NQueens:
    def __init__(self,n):
        self.board, self.queenPositions, self.emptyColumns = self.getNewBoard(n)
        self.n = n

    # use greedy algorithm to initially place queens
    def getNewBoard(self,n):
    # queens are represented as ones in 2d list of all zeros
    # Since it's a 2d list, each element is a row of zeros except for the queen
        board = [ [0] * n for _ in range(n) ]
        queensPos = []
        emptyColumns = [True] * n

        randomIndex = random.randint(0,n-1)
        board[0][randomIndex] = 1
        queensPos.append((0,randomIndex))
        emptyColumns[randomIndex] = False
        for row in range(1,n):
            minConflicts = n
            bestPos = (-1,-1)
            for col in range(n):
                conflicts = self.specificQueenConflicts((row,col),queensPos)
                if conflicts == 0:
                    bestPos = (row,col)
                    break
                else:
                    if conflicts < minConflicts:
                        minConflicts = conflicts
                        bestPos = (row,col)

            board[bestPos[0]][bestPos[1]] = 1
            queensPos.append((bestPos[0], bestPos[1]))
            emptyColumns[bestPos[1]] = False
        # print(board)
        # print(emptyColumns)
        # print(queensPos)
        return (board,queensPos,emptyColumns)

    # returns true if problem is solved and all queens safe, false otherwise
    def allQueensSafe(self): 
        for pos in self.queenPositions:
            if self.UnderAttack(pos):
                return False
        return True

    # checks column conflict
    def attackViaCol(self,pos):
        for queen in self.queenPositions:
            if pos[1] == queen[1] and queen != pos: # last inqueality checks to make sure you arent comparing the same queen
                return True
        return False

    # checks row conflicts
    def attackViaRow(self,pos):
        for queen in self.queenPositions:
            if pos[0] == queen[0] and queen != pos:
                return True
        return False

    # checks diagonal conflicts
    def attackViaDiagonal(self,pos):
        for queen in self.queenPositions:
            if abs(queen[0] - pos[0]) == abs(queen[1] - pos[1]) and queen != pos:
                return True
        return False

    # checks all conflicts by calling 3 attack methods above that check specific rows/columns/diagonals
    def UnderAttack(self,position):
        if self.attackViaDiagonal(position):
            return True
        if self.attackViaRow(position):
            return True
        if self.attackViaCol(position):
            return True

        return False

    # returns number of pieces attacking queen at position pos
    # otherQueens is an actual array when the constructor calls this function
    def specificQueenConflicts(self,pos,otherQueens = None): 

        # this just differentiates from when the constructor calls this function vs when solveBoard() calls it
        # only to prevent duplicate code
        allQueens = []
        if otherQueens:
            allQueens = otherQueens
        else:
            allQueens = self.queenPositions

        count = 0
        for queen in allQueens:
            if queen == pos:
                continue
            if abs(queen[0] - pos[0]) == abs(queen[1] - pos[1]):
                count += 1
            if pos[0] == queen[0]:
                count += 1
            if pos[1] == queen[1]:
                count += 1

        return count

    # returns position of random queen
    def pickRandomQueen(self): 
        newIndex = random.randint(0,self.n - 1)
        return self.queenPositions[newIndex]

    #return positions of all the queens 
    def returnPositions(self):
        return self.queenPositions

    # moves quen from startPos to endPos
    # isActualMove is True only when a final move decision has been made
    # isActualMove is False when the move is only to check conflicts 
    # this distiction prevents updating empty columns on moves which are only to check conflict
    def moveQueen(self,startPos,endPos,isActualMove=False): 
        assert self.board[startPos[0]][startPos[1]] == 1
        # above assert will fail if the start position does not have a queen

        self.board[startPos[0]][startPos[1]] = 0
        self.board[endPos[0]][endPos[1]] = 1
        self.queenPositions.remove(startPos)
        self.queenPositions.append(endPos)

        if isActualMove:
            self.emptyColumns[endPos[1]] = False
            self.updateEmptyColumns(startPos)


    def availablePositions(self,pos):
        # returns list of tuples with all positions queen can go
        # queen can only move to different columns on its respective row
        availablePos = []
        for x in range(self.n):
            availablePos.append((pos[0],x))

        return availablePos

    # same thing as availablePositions() except you only return those with empty columns
    def emptyColumnPositions(self,pos):
        availablePos = []
        for x in range(self.n):
            if self.emptyColumns[x]:
                availablePos.append((pos[0],x))

        return availablePos

    # checks if the column where the queen moved from is now empty, if it is then update
    def updateEmptyColumns(self,pos):
        col = pos[1]
        for row in range(self.n):
            # if there is a queen on any row at that specific column, then don't update
            if self.board[row][col] == 1:
                return

        self.emptyColumns[col] = True


# min conflicts solver
def solveBoard(size):
    n = size
    NQ = NQueens(n) # create initial board of size nxn
    moves = 0
    print("Starting...")
    while not NQ.allQueensSafe():
        if moves > 100:
            print("Resetting...")
            moves = 0
            NQ = NQueens(n) # reset board since on average a board can be solved in around 50 moves, prevents getting stuck

        pickedQueen = NQ.pickRandomQueen()
        minConflictPosition = (-1,-1)
        positions = NQ.availablePositions(pickedQueen)  

        found = False #skip the next rest of the search heuristics if a position has been found

        # look first for 0 conflict positions using "emptyColumns" (taken from NASA paper)
        emptyColPositions = NQ.emptyColumnPositions(pickedQueen)
        for pos in emptyColPositions:
            NQ.moveQueen(pickedQueen,pos) # move queen
            newNumberOfConflicts = NQ.specificQueenConflicts(pos)
            NQ.moveQueen(pos,pickedQueen) # move queen back
            if newNumberOfConflicts == 0:
                found = True
                minConflictPosition = pos
                break
        
        # if 0 conflict positions cannot be found, then randomly sample for 1 conflict positions
        # usually found pretty quickly though theoretically can go on forever (taken from NASA paper)
        samples = 0
        while not found and samples < n:
            randomIndex = random.randint(0,n-1)
            pos = positions[randomIndex]
            NQ.moveQueen(pickedQueen,pos) # move queen
            newNumberOfConflicts = NQ.specificQueenConflicts(pos)
            NQ.moveQueen(pos,pickedQueen) # move queen back
            if newNumberOfConflicts == 1:
                found = True
                minConflictPosition = pos
            samples+=1


        minAttacks = n + 1 # n + 1 is greater than any possibility of attacks so this is guaranteed to get minimized
        #normal search through all positions (while staying in the same row)
        if not found:
            for pos in positions: # iterate through all positions of pickedQueen and move to position of minimum conflict
                NQ.moveQueen(pickedQueen,pos)
                newNumberOfConflicts = NQ.specificQueenConflicts(pos)
                if newNumberOfConflicts < minAttacks:
                    minConflictPosition = pos
                    minAttacks = newNumberOfConflicts
                NQ.moveQueen(pos,pickedQueen) # move queen back

        NQ.moveQueen(pickedQueen,minConflictPosition,True)# move queen to least conflict spot
        # print(moves)
        moves+=1    

    pos = NQ.queenPositions
    for p in pos:
        print(p)
    return pos

def main():
    cwd = os.getcwd().replace('\\', '/') # gets the current working directory of this python file

    f1 = open(cwd + "/nqueens.txt", mode='r') # opens the nqueens file to read the n's from
    nums = [line.rstrip('\n') for line in f1]
    print(nums)

    f2 = open(cwd + "/nqueens_out.txt", mode='w+') # creates an output file for the matrices to be placed in

    # writes the solution to each size n to the output file
    for n in nums:
        start = time.time()
        print(n)
        positions = solveBoard(int(n))
        f2.write(n+'\n')
        for p in positions:
            f2.write(str(p)+'\n')
        end = time.time()
        print("Took " + str(end-start) + " seconds to execute")
    f2.close()

main()
