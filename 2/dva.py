# General idea 
#   pt I
#   For game to be possible, all picks in all plays 
#   within each line/game have to be lower/equal to total available
# 
#   Each line has 'Game [ID]':
#   ; divide games
#   , divide picks within game
#   
#   Count += [ID]s of possible games
#
#   pt II
#   within each line find the highest number for corresponding color and 
#   return power of all three colors  for each line

# Variables
#FILE_NAME = "input.small.txt"
FILE_NAME = "input.txt"

ID_DELIMITER    = ':'
GAME_DELIMITER  = ';'
PICK_DELIMITER  = ','

COLOR_RED   = "red"
COLOR_GREEN = "green"
COLOR_BLUE  = "blue"

############## PART I #############
ROW_HEADER_EXAMPLE = 'Game 1'

Count_ColorCube_Dict = {
    COLOR_RED   : 12,
    COLOR_GREEN : 13,
    COLOR_BLUE  : 14
}

def PlayLineFromPos(row, startPos):
    isLineGood = True

    row = row[startPos:]
    row = row.split()
    # print(row)

    # arrLen = len(row)
    # print(arrLen)
    
    arrPointer = 1      # 0 is ID_DELIMITER
    
    Game_Dict = {
        COLOR_RED   : 0,
        COLOR_GREEN : 0,
        COLOR_BLUE  : 0
    }

    ### "endless" while
    while True:
        cubeCount               = int(row[arrPointer])        
        cubeColorWithDivider    = row[arrPointer + 1]         
        arrPointer += 2

        # print(cubeCount, cubeColorWithDivider)

        # get color as key usable in dictionary
        cubeColorKey = cubeColorWithDivider.replace(',', '')    
        cubeColorKey = cubeColorKey.replace(';', '')            
        
        Game_Dict[cubeColorKey] += cubeCount

        #### CASE ,         => next cubes
        if (PICK_DELIMITER in cubeColorWithDivider):
            continue
        
        #### CHECK GAME CONDITIONS
        if (Game_Dict[COLOR_RED] > Count_ColorCube_Dict[COLOR_RED]):
            isLineGood = False

        if (Game_Dict[COLOR_GREEN] > Count_ColorCube_Dict[COLOR_GREEN]):
            isLineGood = False
        
        if (Game_Dict[COLOR_BLUE] > Count_ColorCube_Dict[COLOR_BLUE]):
            isLineGood = False
        


        #### CASE ;         => next pick
        if (isLineGood == True      and     GAME_DELIMITER in cubeColorWithDivider):
            ##### reset pick stats
            Game_Dict[COLOR_RED]    = 0
            Game_Dict[COLOR_GREEN]  = 0
            Game_Dict[COLOR_BLUE]   = 0

            continue


        #### CASE default   => end game
        break

    return isLineGood

## Core game-play
def PlayGame(FileName):
    
    file = open(FileName, 'r')         
    
    startRdPos = len(ROW_HEADER_EXAMPLE) - 1     # precaution of whitespace ignore
    idSum = 0

    ### "endless" while
    while True:
        #### Load file (line by line - memory efficient)
        line = file.readline()

        #### if line is null => end while
        if not line:
            break

        #### Get game ID by building all string from 'Game ' till ':'
        endRdPos = line.find(ID_DELIMITER)

        builtId = ""       
        for x in range(startRdPos, endRdPos):
            builtId += str(line[x])
        
        #### Start playing actual game
        lineResult = PlayLineFromPos(line, endRdPos)

        if (lineResult == True):
            idSum += int(builtId)

    return idSum



############## PART II ############
##
def GetMinimumPossiblePerRow(row, startPos):
    row = row[startPos:]
    row = row.split()
    # print(row)

    arrLen = len(row)
    # print(arrLen)
    
    arrPointer = 1      # 0 is ID_DELIMITER
    
    Min_Game_Dict = {
        COLOR_RED   : 0,
        COLOR_GREEN : 0,
        COLOR_BLUE  : 0
    }

    ### "endless" while
    while True:
        cubeCount               = int(row[arrPointer])        
        cubeColorWithDivider    = row[arrPointer + 1]
        arrPointer += 2
        
        # get color as key usable in dictionary
        cubeColorKey = cubeColorWithDivider.replace(',', '')
        cubeColorKey = cubeColorKey.replace(';', '')

        if (Min_Game_Dict[cubeColorKey] < cubeCount):
            Min_Game_Dict[cubeColorKey] = cubeCount

        #### CASE ,         => next cubes
        if (PICK_DELIMITER in cubeColorWithDivider):
            continue
        
        #### CASE ;         => next cubes
        if (GAME_DELIMITER in cubeColorWithDivider):
            continue

        #### CASE default   => end game
        break
    
    return Min_Game_Dict[COLOR_RED] * Min_Game_Dict[COLOR_GREEN] * Min_Game_Dict[COLOR_BLUE]

##
def PlayGamePtII(FileName):

    file = open(FileName, 'r')         
    
    minSum = 0

    ### "endless" while
    while True:
        #### Load file (line by line - memory efficient)
        line = file.readline()

        #### if line is null => end while
        if not line:
            break

        #### Get game ID by building all string from 'Game ' till ':'
        endRdPos = line.find(ID_DELIMITER)
        
        #### Start playing actual game
        lineResult = GetMinimumPossiblePerRow(line, endRdPos)

        minSum += lineResult

    return minSum


############## INITIAL CODE ############
if __name__ == "__main__":
    # part I
    sumOfPossible = PlayGame(FILE_NAME)
    print(f"Sum of all IDs of possible games: {sumOfPossible}")

    # part II
    sumOfMinPossible = PlayGamePtII(FILE_NAME)
    print(f"Sum of minimum required cube powers (R * G * B) (for game to be possible) of input file is: {sumOfMinPossible}")