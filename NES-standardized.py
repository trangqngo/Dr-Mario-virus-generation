#This code is based on the standardized pseudocode included in the NES algorithm section
#the generation of a random cell must be put into the fillBottle function
#rather than the addVirus function because of the preferred color cycle 
#changes the state (of the seed)


from __future__ import print_function
import sys    # command-line arguments
import random # generating a random seed

global bottle, state, numRows, numCols, colorPrefer, numVirus

def random_init(seed):
    global state

    # Convert the decimal value seed into a list of binary bits.
    state = [int(b) for b in bin(seed)[2:]]

    # The state should be 16-bits so pad with a prefix if necessary.
    leading_zeros = 16 - len(state)
    state = leading_zeros*[0] + state

def random_increment():
	global state

	# tap bit 7 and bit 15
	bit9 = state[6]
	bit1 = state[14]
	newbit = bit1 ^ bit9

	# rotate in the new output bit
	state = [newbit] + state[0:15]


def random_row(max_value = 15):
    random_increment()
    value = 8*state[4] + 4*state[5] + 2*state[6] + 1*state[7]
    while value > max_value:
        random_increment()
        value = 8*state[4] + 4*state[5] + 2*state[6] + 1*state[7]
    return value

def random_col():
    value = 4*state[13] + 2*state[14] + 1*state[15]
    return value

def random_index():
    random_increment()
    value = 8*state[12] + 4*state[13] + 2*state[14] + 1*state[15]
    return value

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
        r = (r - 1) % 16
        if r == 15: #end of bottle, not cyclic so stops here
            return (None, None)
    return (r,c)

def addVirusNES(r,c,colorPrefer):
    global bottle, numCols, numRows, state
  
    # R = random({0,1,...,numRows-1})
    # C = random({1,2,...,numCols-1})
    #get candidate cell 
    # R = random_row(numRows-1)
    # C = random_col()
    #get empty cell starting from candidate cell 
    #(r,c) = nextEmptyRightDown(R,C) 
    #(r,c) = (R,C)
    while (r,c) != (None, None): #if not at end of bottle
        colorTry = 0
        color = colorPrefer
        #try all 3 colors for (r,c) in preferred sequence
        while colorTry < 3:
            #color = (colorPrefer+colorOffset) % 3
            if isAvailable(r, c, color):
                bottle[r][c] = color
                return color
            #switch to next color in sequence of preferered colors
            if color == 0: color = 2
            elif color == 1: color = 0
            else: color = 1
            colorTry += 1
        #(r,c) can't have any colors, increment to next cell 
        #if nextEmptyRightDown here then will keep returning (r,c)
        (r,c) = nextCellRightDown(r,c)
    return None #no empty cell for this color


#input: one seed at a time
def fillBottleNES():
    global numVirus, numRows
    colorTable = [0,1,2,2,1,0,0,1,2,2,1,0,0,1,2,1]
    #colorPrefer = 0
    numRemain = numVirus
    while numRemain > 0:
        #get candidate cell
        R = random_row(numRows-1)
        C = random_col()
        colorPrefer = numRemain % 4
        #choose preferred virus color
        if numRemain % 4 == 3:
            i = random_index()
            colorPrefer = colorTable[i]
        #try to add virus color to candidate cell 
        if addVirusNES(R,C,colorPrefer) != None:
            numRemain = numRemain - 1  
          
                      
    return 

def initPuzzleNES(levelNum):
    global numRows, numCols, numVirus, bottle
    print("level "+str(levelNum)) 
    assert levelNum >= 0 and levelNum <= 30
    numRows = 10
    if levelNum >= 15: numRows += 1
    if levelNum >= 17: numRows += 1
    if levelNum >= 19: numRows += 1
    numCols = 8
    numVirus = min(levelNum,20)*4 + 4
    bottle = [[None for i in range(8)] for j in range(16)]

def genPuzzleNES(levelNum):
    global numRows, numCols, bottle, seedList, colorPrefer, numVirus
    initPuzzleNES(levelNum)
    colorPrefer = 0
    numRemain = numVirus
    fillBottleNES()
    return bottle

def printBottle():
    global bottle, numCols
    res = ""
    for row in reversed(bottle):
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
    # If 1 parameter is given, then it is just the name of the script.
    # If 2 parameter are given, then the 2nd is the level.
    # If 3 parameters are given, then the 2nd + 3rd are the seed.
    # If 4 parameters are given, then the 2nd is level, and 3rd + 4th the seed.

    # Level: Read from command-line or set to 20 by default.
    if len(sys.argv) == 2:
        levelNum = int(sys.argv[1])
    elif len(sys.argv) == 4:
        levelNum = int(sys.argv[3])
    else:
        levelNum = 20

    # Seed: Read from command-line or randomly generate.
    # s0 s1 are decimal values; seed0 seed1 are hex strings to match bottle.c.
    # https://stackoverflow.com/questions/209513/convert-hex-string-to-int-in-python
    # https://stackoverflow.com/questions/11676864/how-can-i-format-an-integer-to-a-two-digit-hex
    if len(sys.argv) in [3,4]:
        s0 = int(sys.argv[1], 16)
        s1 = int(sys.argv[2], 16)
    else:
        s0 = random.randint(0,255)
        s1 = random.randint(0,255)
    seed0 = "{:02x}".format(s0)
    seed1 = "{:02x}".format(s1)

    # Compute the numeric value of the seed in decimal.
    seed = 256*int(seed0,16) + int(seed1,16)
    random_init(seed)
    print("seed is "+str(seed))
    print(seed0.upper() + ", " + seed1.upper())
    genPuzzleNES(levelNum)
    printBottle()
