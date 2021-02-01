
#This code is based on the standardized pseudocode included in the N64 algorithm section
#TODO: take level and seed as input
#TODO: infinite loop lvl 22 seed 5678

#randomization code

import math, sys

global randomIndex, randomTable, RMAX

def randomize00():
    global randomIndex, randomTable, RMAX
    for i in range(24):
        j = randomTable[i] - randomTable[i + 31]
        if j >= 0: randomTable[i] = j
        else: randomTable[i] = j + RMAX
    for i in range(24,55):
        j = randomTable[i] - randomTable[i - 24]
        if j >= 0: randomTable[i] = j
        else: randomTable[i] = j + RMAX
    return

def randomSeed(s):
    global randomIndex, randomTable, RMAX
    randomTable[54] = s
    k = 1
    for i in range(1,55):
        j = (21 * i % 55) - 1
        randomTable[j] = k
        k = s - k
        if (k < 0): k += RMAX
        s = randomTable[j]
    randomize00()
    randomize00()
    randomize00()
    randomize00()
    randomIndex = 0
    return

def irandom():
    global randomIndex, randomTable, RMAX
    randomIndex = randomIndex + 1
    if randomIndex >= 55:
        randomize00()
        randomIndex = 0
    return (randomTable[randomIndex] & 0xffff)

def trandom(n):
    global randomIndex, randomTable, RMAX
    #print((n * irandom()) >> 16)
    return ((n * irandom()) >> 16)

##################################################

#virus generation code

global bottle, numCols, numRows, numVirus

def isAvailable(r,c,color):
    global bottle, numRows, numCols
    if bottle[r][c] != None:
        return False
    cset = set([0,1,2])
    if r >= 2:
        cset.discard(bottle[r-2][c])
    if c >= 2:
        cset.discard(bottle[r][c-2])
    if r < 17 - 2:
        cset.discard(bottle[r+2][c])
    if c < numCols - 2:
        cset.discard(bottle[r][c+2])
    return color in cset

#return the next cell
# or (None, None) if the next cell will be outside of the bottle
def nextCellUpRight(r, c):
    global numCols, numRows
    r = (r - 1)
    if r == 17 - numRows - 1:
        r = numRows - 1
        c = (c + 1) % numCols
        if c == 0:
            return (None, None) #end of infectible region
    return (r,c)

#return the next available cell or (None, None) if at the end of table
def nextAvailableUpRight(r, c, color):
    global numRows, numCols
    while not isAvailable(r, c, color):
        (r, c) = nextCellUpRight(r, c)
        if (r,c) == (None, None): #end of infectible region
            return (None, None)
    return (r, c)

def addVirusN64(numRemainColor):
    global bottle, numRows, numCols
    attempts = 0
    while attempts < 8:
        #choose one color that has not reached its quota
        color = trandom(3)
        while numRemainColor[color] == 0:
            color = trandom(3)
        #brute force phase
        if attempts == 2 or attempts == 5:
            (r,c) = nextAvailableUpRight(16,0,color)
            if (r,c) != (None, None):
                bottle[r][c] = color
                return color
        #random placement phase
        else:
            #R = random({0,1,...,numRows-1})
            #C = random({0,1,...,numCols-1})
            #get candidate cell - in bounds
            #Double check where and how many times trandom() is called
            C = trandom(8)
            R = trandom(17)
            while R < 17 - numRows: #row too high in bottle
                R = trandom(17)
            #if candidate cell is not empty, keep getting new candidate cell
            while bottle[R][C] != None:
                C = trandom(8)
                R = trandom(17)
                while R < 17 - numRows:
                    R = trandom(17)
            if isAvailable(R, C, color): #isAvailable redundantly check isEmpty here
                bottle[R][C] = color
                return color
        attempts += 1
    return None


def fillBottleN64():
    global numVirus
    numRemain = numVirus
    thirdRemain = math.floor(numVirus/3)
    numRemainColor = [thirdRemain]*3
    #choosing one or two extra colors to have extra viruses
    numExtra = numVirus % 3 #number of virus colors with extra viruses
    for _ in range(1,numExtra+1):
        c = trandom(3)
        if numRemainColor[c] <= numRemainColor[(c+1)%3] and numRemainColor[c] <= numRemainColor[(c+2)%3]:
            numRemainColor[c] += 1
    color = 0
    while numRemain > 0:
        addedColor = addVirusN64(numRemainColor)
        if addedColor == None:
            return numRemain
        numRemain -= 1
        numRemainColor[addedColor] -= 1
    return numRemain

def initPuzzleN64(levelNum):
    global bottle, numCols, numRows, numVirus
    numRows = 10
    if levelNum >= 15: numRows += 1
    if levelNum >= 17: numRows += 1
    if levelNum >= 19: numRows += 1
    numCols = 8
    numVirus = min(levelNum,23)*4 + 4
    bottle = [[None for i in range(8)] for j in range(17)]

def genPuzzleN64(levelNum):
    global bottle, numVirus
    initPuzzleN64(levelNum)
    numRemain = fillBottleN64()
    return bottle

def printBottle():
    global bottle, numCols
    res = ""
    for row in bottle:
        res+="#"
        for value in row:
            if value == None: res+= "-"
            if value == 0: res += "Y"
            if value == 1: res += "R"
            if value == 2: res += "B"
        res+="#"
        res+="\n"
    #bottom wall
    for _ in range(numCols+2):
        res+="#"
    print(res)

if __name__ == "__main__":
    randomIndex = 0
    randomTable = [0]*55
    RMAX = 65536
    seed = 1234
    randomSeed(seed)
    genPuzzleN64(22)
    printBottle()
