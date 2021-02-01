#This code is based on the standardized pseudocode included in the SNES algorithm section

import sys

global bottle, seed, numRows, numCols, numVirus

def randomize():
    global seed
    seed = (seed * 5 + 28947) % 65536 #Randomization algorithm
    return

def isAvailable(r,c,color):
    global numRows, numCols
    if bottle[r][c] != None:
        return False
    cset = set([0,1,2])
    if r >= 2:
        cset.discard(bottle[r-2][c])
    if c >= 2:
        cset.discard(bottle[r][c-2])
    if r < numRows - 2:
        cset.discard(bottle[r+2][c])
    if c < numCols - 2:
        cset.discard(bottle[r][c+2])
    return color in cset

#the bottle in memory and the bottle on screen are reversed (*)
#so right-up wrt the bottle on screen translates to right-down wrt bottle in memory
#(*) is due to the SNES algo not using the random index (from seed) to index into bottle
#but to index into another table whose entries are used to index into the bottle
#that table is the bottle reversed
#view NextVirusPosTable in nightmareci's C code
def nextCellRightUpCyclic(r, c):
    global numCols, numRows
    c = (c + 1) % numCols
    if c == 0:
        r = (r + 1) % numRows
    return (r,c)


#return next available cell for color 
#or None if no avail cells for color in entire bottle 
def nextAvailableRightUpCyclic(r, c, color):
    (R, C) = (r, c) #initial spot
    while isAvailable(r, c, color) == False:
        (r, c) = nextCellRightUpCyclic(r, c)
        if (r, c) == (R, C):
            return (None,None)
    return (r, c)

def addVirusSNES(color):
    global bottle, seed, numRows, numCols
    # R = random({0,1,...,numRows-1})
    # C = random({0,1,...,numCols-1})
    randomize()
    loc = (seed + 1) % (numRows*numCols)
    #NOTE: start scanning for available cell AFTER (R,C)
    R = loc // numCols
    C = loc % numCols + 1
    if C == 8:
        R = (R + 1) # numRows
        C = 0
        #reached end of bottle, loops 
        if R == numRows:
            R = 0
    fails = 0
    while fails < 3:
        (r,c) = nextAvailableRightUpCyclic(R,C,color)
        if (r,c) == (None,None):
            fails = fails + 1
            color = (color + 1) % 3
        else:
            bottle[r][c] = color
            return color
    return None

def fillBottleSNES(numVirus):
    color = 0
    numRemain = numVirus
    while numRemain > 0:
        if addVirusSNES(color) != None:
            #added virus
            numRemain = numRemain - 1
            color = (color + 1) % 3
        else: #did not add virus
            break
    return numRemain

def initPuzzleSNES(levelNum):
    global numRows, numCols, bottle, numVirus
    numRows = 10
    if levelNum >= 15: numRows += 1
    if levelNum >= 17: numRows += 1
    if levelNum >= 19: numRows += 1
    numCols = 8
    numVirus = min(levelNum,23)*4 + 4
    bottle = [[None for i in range(8)] for j in range(16)]

def genPuzzleSNES(levelNum):
    global numRows, numCols, bottle, numVirus
    initPuzzleSNES(levelNum)
    numRemain = fillBottleSNES(numVirus)
    return bottle

def printBottle():
    global bottle, numCols
    res = ""
    for row in reversed(bottle):
        res+="#"
        for value in row:
            if value == None: res+= "."
            if value == 0: res += "R"
            if value == 1: res += "Y"
            if value == 2: res += "B"
        res+="#"
        res+="\n"
    #bottom wall
    for _ in range(numCols+2):
        res+="#"
    print(res)

if __name__ == "__main__":
    level = int(sys.argv[1])
    seed = int(sys.argv[2],16)
    genPuzzleSNES(level)
    printBottle()
