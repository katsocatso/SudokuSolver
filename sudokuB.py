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

###############################################################################################

# Prints the matrix prettily
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

# Checks if val is in col colIdx
def valInCol(colIdx, val, matrix):
    for row in matrix:
        if val == row[colIdx]:
            return True
    return False

# Checks if val is in row rowIdx
def valInRow(rowIdx, val, matrix):
    return val in matrix[rowIdx]

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
        
############################################################################################
'''
Functions for finding all blank cells / all possible values for cels in the matrix
'''
# Remove values from possible values for its neighbour cells (i.e. cells in the same row, col, or box)
# Returns the updated version of allPossibleValues after such values are removed
def removeValue(row, col, val, matrix, allPossibleValues):
    # Remove value from same row
    for c in range(len(matrix[row])):
        key = str(row) + str(c)
        if key in allPossibleValues and val in allPossibleValues[key]:
            allPossibleValues[key].remove(val)

    # Remove value from same col
    for r in range(len(matrix)):
        key = str(r) + str(col)
        if key in allPossibleValues and val in allPossibleValues[key]:
            allPossibleValues[key].remove(val)

    # Remove value from same box
    boxIdx = getBox(row, col)
    shift = boxIdx % 3
    for r in range(3):
        for c in range(3):
            key = str(r + boxIdx - shift) + str(c + shift * 3)
            if key in allPossibleValues and val in allPossibleValues[key]:
                allPossibleValues[key].remove(val)
    return allPossibleValues


# Returns the dictionary of all possible values for every blank cell in the matrix
# allPossibleValues key is "<row><col>" (a string) and its value is a list of possible
#   values for the cell at [row, col]
def initializeAllPossibleValues(matrix, blanks):
    allPossibleValues = {}
    # For every blank cell, set possible values to entire domain
    for x in blanks:
        rowColStr = str(x[0]) + str(x[1])
        allPossibleValues[rowColStr] = copy.deepcopy(DOMAIN)

    # Remove values based on cells that are not blank in matrix
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if matrix[r][c] != BLANK:
                val = matrix[r][c]
                allPossibleValues = removeValue(
                    r, c, val, matrix, allPossibleValues)
    return allPossibleValues

# Returns a list of all the blank cells in the matrix
def findAllBlanks(matrix):
    blanks = []
    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            if matrix[r][c] == BLANK:
                blanks.append([r, c])
    return blanks

############################################################################################
'''
Random generation functions
'''
# Returns a random blank cell from the given list of all blank cells in the matrix
def findRandBlank(blanks):
    return blanks[random.randint(0, len(blanks) - 1)]

# Returns a random value out of possibleValuesForCell
def findRandomVal(possibleValuesForCell):
    randValIdx = random.randint(0, len(possibleValuesForCell) - 1)
    return possibleValuesForCell[randValIdx]

############################################################################################
'''
Forward checking functions
'''

# Checks if any cells in currRow will have an empty assignment after val is removed
def forwardCheckRow(currRow, currCol, val, allPossibleValues):
    for c in range(9):
        # If cell is [currRow, currCol] then ignore
        if c == currCol:
            continue
        key = str(currRow) + str(c)
        if key in allPossibleValues:
            if len(allPossibleValues[key]) == 1 and val in allPossibleValues[key]:
                return False
    return True

# Checks if any cells in currCol will have an empty assignment after val is removed
def forwardCheckCol(currRow, currCol, val, allPossibleValues):
    for r in range(9):
        # If cell is [currRow, currCol] then ignore
        if r == currRow:
            continue
        key = str(r) + str(currCol)
        if key in allPossibleValues:
            if len(allPossibleValues[key]) == 1 and val in allPossibleValues[key]:
                return False
    return True

# Checks if any cells in the same box as currRow, currCol will have an empty assignment after val is removed
def forwardCheckBox(currRow, currCol, val, allPossibleValues):
    currBox = getBox(currRow, currCol)
    shift = currBox % 3
    for r in range(3):
        for c in range(3):
            rowExpr = r + currBox - shift
            colExpr = c + shift * 3

            if rowExpr == currRow and colExpr == currCol:
                continue

            key = str(rowExpr) + str(colExpr)
            if key in allPossibleValues:
                if len(allPossibleValues[key]) == 1 and val in allPossibleValues[key]:
                    return False
    return True

# Checks if any cells in the matrix will have an empty assignment after val is removed
def forwardCheck(currRow, currCol, val, allPossibleValues):
    if forwardCheckRow(currRow, currCol, val, allPossibleValues):
        if forwardCheckCol(currRow, currCol, val, allPossibleValues):
            if forwardCheckBox(currRow, currCol, val, allPossibleValues):
                return True
    return False
############################################################################################

# Modifies the global var nodesExpanded
# Returns true if the Sudoku puzzle is solvable, false otherwise
def tryAssign(matrix):
    global nodesExpanded

    # Find all blank cells in the matrix
    blanks = findAllBlanks(matrix)

    # if list of blanks is empty, we're done and assigned all blanks in the puzzle
    if not blanks:
        print("Total Nodes expanded: ", nodesExpanded)
        return True

    # Get random blank cell
    nextBlank = findRandBlank(blanks)
    row = nextBlank[0]
    col = nextBlank[1]
    rckey = str(row) + str(col)

    allPossibleValues = initializeAllPossibleValues(matrix, blanks)
    possibleValuesForCell = allPossibleValues[rckey]

    # Pick random value and assign it to the chosen blank cell until there are no possible values left
    while possibleValuesForCell:
        val = findRandomVal(possibleValuesForCell)
        possibleValuesForCell.remove(val)

        matrix[row][col] = val
        nodesExpanded += 1
        print(nodesExpanded)        # Can comment this out for no continous output

        validAssignment = forwardCheck(
            row, col, val, allPossibleValues)
        # if there are no values left for a particular cell
        if not validAssignment:
            matrix[row][col] = 0
            continue

        if tryAssign(matrix):
            return True

        matrix[row][col] = 0
    return False


def versionB():
    global allPossibleValues
    global blanks
    matrix = []
    for line in sys.stdin:
        rowAsStr = line.strip().split(" ")
        matrix.append([int(x) for x in rowAsStr])
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
versionB()
endTime = time.time()
executionTime = endTime - startTime
print("Execution Time:", executionTime)
