#This code is based on the standardized pseudocode included in the Game Boy algorithm section
#input: a list of seeds/ a file of seeds
#input is a bit different from the standardized code because of 
#the different randomization technique in the GameBoy
#(the seed is fetched one at a time)

import sys, random

global bottle, seedList, numRows, numCols, levelNum, colorPrefer, numVirus

def randomIndex(seed):
    #print("randomIndex")
    global numRows, numCols

    swappedNibbleSeed = (seed//16)+(seed%16)*16
    b = swappedNibbleSeed % 16 # & 0x0F for level 25-30 (buggy)
    if levelNum == 30: a = seed & 0xFE
    elif levelNum == 29: a = seed & 0x0A
    elif levelNum == 28: a = seed & 0xC1
    elif levelNum == 27: a = seed & 0xD1
    elif levelNum >= 25: a = seed & 0xE5
    else:
        b = swappedNibbleSeed % 64 # & 0x3F for level 0-24
        if levelNum >= 22: #a = seed % 16 + (seed // 32)%2*32 #& 0x2F
            a = seed & 0x2F
        elif levelNum >= 19: # a = seed % 8 + (seed // 32)%2*32 #& 0x27
             a = seed & 0x27
        elif levelNum >= 17: #a = seed % 32 #& 0x1F
             a = seed & 0x1F
        elif levelNum >= 15:   #a = seed % 8 + (seed // 16)%2*16 #& 0x17
             a = seed & 0x17
        else:  #a = seed % 16 #& 0x0F
             a = seed & 0x0F
    pos = 0x7F - (a+b)
    if (pos > 127) or (pos < 0): #if index outside of the bottle
        #in the asm code, this is taken care of by checking if pos is FF (empty)
        return None
    return pos

#isAvailable AND nextEmptyRightDown both check whether the cell is empty 
#redundant 
def isAvailable(r,c,color):
    global bottle, numRows, numCols
    #empty?
    if bottle[r][c] != None:
        return False
    cset = set([0,1,2])
    #2-away rule? 
    if r >= 2:
        cset.discard(bottle[r-2][c])
    if c >= 2:
        cset.discard(bottle[r][c-2])
    if r < numRows - 2:
        cset.discard(bottle[r+2][c])
    if c < numCols - 2:
        cset.discard(bottle[r][c+2])
    return color in cset

#return the next cell 
#or None if reached the end of the bottle 
def nextCellRightDown(r, c):
    global numRows, numCols
    c = (c + 1) % numCols
    if c == 0:
        r = (r + 1) % 16
        if r == 0: #end of bottle, not cyclic so stops here
            return (None, None)
    return (r,c)


#if (r,c) can't have any color and IS empty then infinite loop here
#remove this helper function and delegate checking if cell is empty to isAvailable?
# def nextEmptyRightDown(r, c):
#     #print("nextEmptyRightDown")
#     global bottle, numCols, numRows
#     while bottle[r][c] != None:
#         #if (r, c) == (0, numCols-1): #if end of bottle
#         if r == (numRows - 1) and c == (numCols-1):
#             return (None, None)
#         (r, c) = nextCellRightDown(r, c)
#     return (r, c)


def addVirusGB(colorPrefer,seed):
    global bottle, numCols, numRows
    # R = random({0,1,...,numRows-1})
    # C = random({1,2,...,numCols-1})
    #get random index into the bottle 
    loc = randomIndex(seed)
    if loc == None: #location is outside of the bottle
        #try next seed 
        return False
    #candidate cell is at (R,C)
    R = loc // numCols
    C = loc % numCols
    #get empty cell starting from candidate cell 
    #(r,c) = nextEmptyRightDown(R,C) 
    (r,c) = (R,C)
    while (r,c) != (None, None): #if not at end of bottle
        colorOffset = 0
        #try all 3 colors for (r,c)
        while colorOffset < 3:
            color = (colorPrefer+colorOffset) % 3
            if isAvailable(r, c, color):
                bottle[r][c] = color
                return color
            colorOffset += 1
        #(r,c) can't have any colors, increment to next cell 
        #if nextEmptyRightDown here then will keep returning (r,c)
        (r,c) = nextCellRightDown(r,c)
    return None #no empty cell for this color

#input: one seed at a time
def fillBottleGB(numRemain, seed):
    global bottle, colorPrefer
    # colorPrefer = 0
    # numRemain = numVirus
    if addVirusGB(colorPrefer,seed) != None:
        numRemain = numRemain - 1
        colorPrefer = (colorPrefer + 1) % 3
    return numRemain

def initPuzzleGB(): 
    global levelNum, numRows, numCols, bottle, seedList, colorPrefer, numVirus
    assert levelNum >= 0 and levelNum <= 30
    numRows = 10
    if levelNum >= 15: numRows += 1
    if levelNum >= 17: numRows += 1
    if levelNum >= 19: numRows += 1
    if levelNum > 22: numRows += 1
    numCols = 8
    numVirus = min(levelNum,20)*4 + 4
    bottle = [[None for i in range(8)] for j in range(16)]

def genPuzzleGB():
    global levelNum, numRows, numCols, bottle, seedList, colorPrefer, numVirus
    initPuzzleGB()
    colorPrefer = 0
    numRemain = numVirus
    for seed in seedList: 
        if numRemain == 0: #the puzzle is complete 
            break
        numRemain = fillBottleGB(numRemain, seed)
    return bottle

def printBottle():
    global bottle, numCols
    res = ""
    for row in bottle:
        res+="#"
        for value in row:
            if value == None: res+= "."
            if value == 0: res += "S"
            if value == 1: res += "B"
            if value == 2: res += "W"
        res+="#"
        res+="\n"
    #bottom wall
    for _ in range(numCols+2):
        res+="#"
    print(res)

if __name__ == "__main__":
    levelNum = int(sys.argv[1])
    seedList = [71, 46, 196, 201, 189, 243, 210, 83, 68, 112, 185, 8, 211, 151, 206, 147, 243, 133, 175, 104, 
    205, 96, 78, 150, 198, 6, 182, 95, 101, 111, 4, 21, 114, 104, 40, 21, 84, 92, 6, 42, 195, 76, 203, 156, 77, 1, 61, 97, 174, 16, 76, 181, 213, 139, 188, 166, 172, 39, 220, 63, 39, 52, 48, 14, 253, 68, 227, 135, 198, 57, 32, 90, 253, 148, 32, 89, 174, 73, 59, 64, 71, 254, 246, 60, 88, 141, 21, 74, 50, 106, 239, 205, 147, 137, 31, 132, 22, 20, 155, 112]
    # a = [None]*100
    # for _ in range(0,100):
    #     a[_] = random.randint(0,255)
    # print(a)
    genPuzzleGB()
    printBottle()
