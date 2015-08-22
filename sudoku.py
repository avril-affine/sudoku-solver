from collections import deque

empty = [1,2,3,4,5,6,7,8,9]
quad = [[] for x in xrange(9)]

def makeQuad():
    """constructs an array that has a list of all (i,j)'s for its
       indexes quadrant"""
    for i in xrange(9):
        for j in xrange(9):
            quad[3 * (i // 3) + (j // 3)].append((i,j))

def getQuad(x):
    """returns a list of all (i,j)'s in the inputted (i,j)'s quadrant"""
    i,j = x
    return quad[3 * (i // 3) + (j // 3)]

def getInput(filename):
    """reads in a sudoku puzzle from filename"""
    f = open(filename, "r")
    puzzle = []
    zeros = []
    for i in xrange(9):
        line = f.readline().strip()
        puz_line = []
        for j in xrange(len(line)):
            num = int(line[j])
            if num == 0:
                num = list(empty)
                zeros.append((i, j))
            else:
                num = [num]
            puz_line.append(num)
        puzzle.append(puz_line)
    f.close()
    return (puzzle, zeros)

def getRowVals(puzzle, row):
    """returns list a definite values in the row"""
    row_vals = []
    for box in puzzle[row]:
        if len(box) == 1:
            row_vals.append(box[0])
    return row_vals

def getColVals(puzzle, col):
    """returns list of definite values in the column"""
    col_vals = []
    for x in xrange(9):
        box = puzzle[x][col]
        if len(box) == 1:
            col_vals.append(box[0])
    return col_vals 

def getQuadVals(puzzle, quad):
    """returns list of definite values in quadrant"""
    quad_vals = []
    for coord in quad:
        boxi, boxj = coord
        box = puzzle[boxi][boxj]
        if len(box) == 1:
            quad_vals.append(box[0])
    return quad_vals

def checkRowVals(puzzle, values, i, j):
    """checks if values can be placed anywhere else in row"""
    for val in values:
        check = True
        for col in xrange(9):
            boxi,boxj = (i, col)
            if boxi == i and boxj == j:
                continue
            box = puzzle[boxi][boxj]
            if val in box:
                check = False
                break
        if check:
            values = [val]
            break
    return values

def checkColVals(puzzle, values, i, j):
    """checks if values can be placed anywhere else in column"""
    for val in values:
        check = True
        for row in xrange(9):
            boxi,boxj = (row, j)
            if boxi == i and boxj == j:
                continue
            box = puzzle[boxi][boxj]
            if val in box:
                check = False
                break
        if check:
            values = [val]
            break
    return values

def checkQuadVals(puzzle, values, i, j):
    for val in values:
        check = True
        for coord in getQuad((i, j)):
            boxi,boxj = coord
            if boxi == i and boxj == j:
                continue
            box = puzzle[boxi][boxj]
            if val in box:
                check = False
                break
        if check:
            values = [val]
            break
    return values

def rmValues(values, rmValues):
    """returns list of values with rmValues removed"""
    for val in rmValues:
        if val in values:
            values.remove(val)
    return values
            
def printPuzzle(puzzle):
    for i in xrange(9):
        if i != 0 and i % 3 == 0:
            print "----------------"
        line = ""
        for j in xrange(9):
            box = puzzle[i][j]
            if len(box) == 1:
                line += str(box[0])
            else:
                line += "0"
            if j != 8 and j % 3 == 2:
                line += "|"
            else:
                line += " "
        print line
            
def solution(puzzle, zeros):
    """returns a solved sudoku puzzle"""
    zeros = deque(zeros)
    max_iter = 10 ** 5
    loop = 0
    while zeros:
        loop += 1
        if loop > max_iter:
            break
        i,j = zeros.popleft()
        values = puzzle[i][j]

        # check row
        row_vals = getRowVals(puzzle, i)
        values = rmValues(values, row_vals)
        if len(values) == 1:
            puzzle[i][j] = values
            continue

        # check column
        col_vals = getColVals(puzzle, j)
        values = rmValues(values, col_vals)
        if len(values) == 1:
            puzzle[i][j] = values
            continue

        # check quadrant
        quad_vals = getQuadVals(puzzle, getQuad((i, j)))
        values = rmValues(values, quad_vals)
        puzzle[i][j] = values
        if len(values) == 1:
            puzzle[i][j] = values
            continue

        # check to see if values can be placed anywhere else in row
        values = checkRowVals(puzzle, values, i, j)
        if len(values) == 1:
            puzzle[i][j] = values
            continue

        # check to see if values can be placed anywhere else in column
        values = checkColVals(puzzle, values, i, j)
        if len(values) == 1:
            puzzle[i][j] = values
            continue

        # check to see if values can be placed anywhere else in quadrant
        values = checkQuadVals(puzzle, values, i, j)

        puzzle[i][j] = values
        if len(values) != 1:
            zeros.append((i, j))
    
    return puzzle

def printHRSol(puzzle):
    for i in xrange(9):
        line = ""
        for j in xrange(9):
            box = puzzle[i][j]
            if len(box) == 1:
                line += str(box[0])
            else:
                line += "0"
        print line

if __name__ == '__main__':
    puzzle,zeros = getInput("input3.txt")
    makeQuad()
    sol = solution(puzzle, zeros)
    printPuzzle(sol)
