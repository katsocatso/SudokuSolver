import sys
import random
import copy
import time

'''
Globals and constants
'''
BLANK = 0
DOMAIN = [1, 2, 3, 4, 5, 6, 7, 8, 9]

global nodesExpanded
nodesExpanded = 0
global blanks
blanks = {}

###############################################################################################

def printMatrix(matrix):
    for r in matrix:
        for c in r:
            print(c, end=" ")
        print()

###############################################################################################
'''
Validity checks 
'''
# Checks if val is in box boxIdx
def valInBox(boxIdx, val, matrix):
    box = []
    shift = boxIdx % 3
    for r in range(3):
        for c in range(3):
            box.append(matrix[r + boxIdx - shift][c + shift * 3])
    return val in box

# Returns the box number for [row, col]
# Note: boxes are numbered left to right, top to bottom
# like so:
# 1 2 3
# 4 5 6
# 7 8 9
def getBox(row, col):
    if row < 3:
        if col < 3:
            return 0
        elif col < 6:
            return 1
        else:
            return 2
    elif row < 6:
        if col < 3:
            return 3
        elif col < 6:
            return 4
        else:
            return 5
    elif row < 9:
        if col < 3:
            return 6
        elif col < 6:
            return 7
        else:
            return 8


# Checks if val is in col colIdx
def valInCol(colIdx, val, matrix):
    for row in matrix:
        if val == row[colIdx]:
            return True
    return False

# Checks if val is in row rowIdx
def valInRow(rowIdx, val, matrix):
    return val in matrix[rowIdx]

############################################################################################

# Assigns the list of all the blank cells in the matrix to the global var blanks
def findAllBlanks(matrix):
    global blanks
    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            if matrix[r][c] == BLANK:
                blanks[str(r) + str(c)] = [r, c]

############################################################################################
'''
Random Generation functions
'''

# Returns a random blank cell from the given list of blank cells
def findRandBlank(blanks):
    if not blanks:
        return None
    randBlank = random.choice(list(blanks.keys()))
    return (blanks[randBlank], randBlank)

# Returns a random value out of untriedVals
def findRandomVal(untriedVals):
    idx = random.randint(0, len(untriedVals) - 1)
    return (untriedVals[idx], idx)

############################################################################################

# Modifies the global var blanks and nodesExpanded
# Returns true if the Sudoku puzzle is solvable, false otherwise
def tryAssign(matrix):
    global blanks
    global nodesExpanded
    nextBlankInfo = findRandBlank(blanks)
    if not nextBlankInfo:
        # we're done and assigned all blanks in the puzzle
        print("Total Nodes expanded: ", nodesExpanded)
        return True
    else:
        row = nextBlankInfo[0][0]
        col = nextBlankInfo[0][1]
        nextBlankKey = nextBlankInfo[1]

    untriedVals = copy.deepcopy(DOMAIN)
    while untriedVals:
        val, valIdx = findRandomVal(untriedVals)
        untriedVals.pop(valIdx)

        inCol = valInCol(col, val, matrix)
        inRow = valInRow(row, val, matrix)
        inBox = valInBox(getBox(row, col), val, matrix)

        if not inCol and not inRow and not inBox:
            matrix[row][col] = val
            nodesExpanded += 1
            print(nodesExpanded)

            del blanks[nextBlankKey]

            if tryAssign(matrix):
                return True
            matrix[row][col] = 0
            blanks[str(row) + str(col)] = [row, col]
    return False


def versionA():
    global blanks
    matrix = []
    for line in sys.stdin:
        rowAsStr = line.strip().split(" ")
        matrix.append([int(x) for x in rowAsStr])
    findAllBlanks(matrix)
    solved = tryAssign(matrix)
    if solved:
        printMatrix(matrix)
    else:
        print("Sudoku puzzle not solvable")

############################################################################################
'''
Main program
'''
startTime = time.time()
versionA()
endTime = time.time()
executionTime = endTime - startTime
