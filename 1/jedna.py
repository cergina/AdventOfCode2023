FILE_NAME = "input.txt"

NumberValueDict = {
    'one'   : 1,
    'two'   : 2,
    'three' : 3,
    'four'  : 4,
    'five'  : 5,
    'six'   : 6,
    'seven' : 7,
    'eight' : 8,
    'nine'  : 9
}

def CraftNewString(textToChange):
    newStr = textToChange

    for key in NumberValueDict:
        newStr = newStr.replace(key, key[0] + str(NumberValueDict[key]) + key[-1])
        
    return newStr

def GetFirstNumber(text):
    retVal = 0

    for index, value in enumerate(text):
        if value.isdigit():
            retVal = value
            break
        
    return retVal

# start program
file = open(FILE_NAME, 'r')

sumOfAll = 0

# "endless" while
while True:
    # read line by line (memory efficient)
    line = file.readline()
    
    # if line is null end while
    if not line:
        break
    
    # change one for 1, ...
    line = CraftNewString(line)
    print(line)

    # for loop through line - from start
    first = GetFirstNumber(line)

    # for loop through line - from end
    last = GetFirstNumber(line[::-1])

    # debug print
    #print(f"{first} {last}")

    sumOfAll += int(f"{first}{last}")


print(f"Total is {sumOfAll}")