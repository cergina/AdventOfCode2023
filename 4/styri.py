# General idea
# 
# pt I
# read the file line by line
# divide to two arrays : and | divided
# first part is winning cards and second is the actual cards
# find how many times each line contains actual numbers in the winning numbers
# the rule for X = 0 is Y = 0 |   X = 1 Y = 1 | X = 2 Y = 2 | X = 3 Y = 4 | X = 4 Y = 8 |
# which resembles little bit 2^x behaviour, but more likely 2^(x-1) and only for x > 0
# sum up all the Y
# 
# pt II
# histogram behavior
# we have each card exactly 1 times
# if we are on card 1 and we have winning cards in the actual cards for example 3 times, it means
# we have three other cards , card 2 3 4. So we have card 1  1x, card 2 2x, card 3 2x, card 4 2x, card 5 1x
# 
# so and then we have to bear in mind that even these copies can generate us these additional cards
# (ignore the fact that it could end up having non-existing cards, wont happen)


import numpy as np

# Variables
FROM_VS_CODE = True
# FILE_NAME = "input.small.txt"
FILE_NAME = "input.txt"



class ScratchCard:
    def __init__(self, num, wList, aList):
        self.number = num
        self.winList = wList
        self.actualList = aList


# Functions
## Part I
def PlayGame(fileName):
    
    file = open(fileName, 'r')

    scratchBoardSum = 0
    ignoreLength = len('Card 1') - 1    # ignore 'Card ' (1 is just safety measure)

    # "endless" while
    while True:
        line = file.readline()

        if not line:
            break   # no more lines to process

        ## find out card ID (increments would be sufficient)
        colonPos = line.find(':')
        scratchBoardId = ""

        for x in range(ignoreLength, colonPos):
            scratchBoardId += str(line[x])

        # print(scratchBoardId)

        ## Read actual numbers
        pipePos = line.find('|')

        ## Read 4 winning numbers
        winningPart = line[colonPos + 1:pipePos]
        winningPart = winningPart.split()
        # print(winningPart)

        actualPart = line[pipePos + 1:]
        actualPart = actualPart.split()
        # print(actualPart)

        # How many points we have? double for each point
        linePointsSum = 0

        for key, val in enumerate(actualPart):
            cnt = winningPart.count(val) 
            # print(f"{key} {val} {cnt}")
            linePointsSum += cnt
        
        # How many winning numbers are in actual numbers?
        # print(linePointsSum)

        if (linePointsSum >= 1):
            linePointsSum = 2 ** (linePointsSum - 1)

        objInGen = ScratchCard(linePointsSum, winningPart, actualPart)
        
        # What is the points value of the card?
        # print(linePointsSum)
        
        scratchBoardSum += objInGen.number

    return scratchBoardSum

## Part II
def GetObjectList(fileName):
    
    file = open(fileName, 'r')

    ignoreLength = len('Card 1') - 1    # ignore 'Card ' (1 is just safety measure)
    
    list = []

    # "endless" while
    while True:
        line = file.readline()

        if not line:
            break   # no more lines to process

        ## find out card ID (increments would be sufficient)
        colonPos = line.find(':')
        scratchBoardId = ""

        for x in range(ignoreLength, colonPos):
            scratchBoardId += str(line[x])

        # print(scratchBoardId)

        ## Read actual numbers
        pipePos = line.find('|')

        ## Read 4 winning numbers
        winningPart = line[colonPos + 1:pipePos]
        winningPart = winningPart.split()
        # print(winningPart)

        actualPart = line[pipePos + 1:]
        actualPart = actualPart.split()
        # print(actualPart)

        # How many points we have? double for each point
        linePointsSum = 0

        for key, val in enumerate(actualPart):
            cnt = winningPart.count(val) 
            # print(f"{key} {val} {cnt}")
            linePointsSum += cnt
        
        # How many winning numbers are in actual numbers?
        # print(linePointsSum)

        objInGen = ScratchCard(linePointsSum, winningPart, actualPart)
        list.append(objInGen)

    return list

############## INITIAL CODE ############
if __name__ == "__main__":
    if FROM_VS_CODE == True:
        FILE_NAME = f".\\4\\{FILE_NAME}"

    # part I
    # sumOfPoints = PlayGame(FILE_NAME)
    # print(f"Sum of points in the pile of cards is: {sumOfPoints}")
    
    # part II
    # - process from 1 till end
    obList = GetObjectList(FILE_NAME)
    #print(obList)

    ## we have one of each card at the start
    hist = np.ones(len(obList), dtype=int)
    
    ## lets find out how many we have of the next
    histLen = len(hist)
    print(hist)

    
    for k, v in enumerate(obList):
        print("We are on index ", k, v.number)

        if (k + 1) < histLen:
            for i in range(v.number):
                print(k + 1 + i)
                hist[k + 1 + i] += hist[k]
        # print(hist)
        

    # print(hist)

    print(np.sum(hist))