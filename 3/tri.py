import numpy as np
# General idea
#
#   PART I
#   [X] 1) scan through the file (put it into 2D array)
#   [X] 2) in 2D array => create list of numbers/objects (its value, start pos [X;Y], length)) for row X
#   [X] 3) go through the object list => check all positions around the number (if valid indexes)
#           - if it contains any non-digit, non-'.' character mark attribute IsPartNumber = True
#   [X] 4) sum all the objects (numbers) of valid part numbers
#
#   PART II
#   [X] 1) scan through the file (put it into 2D array)
#   [X] 2) in 2D array => create list of numbers/objects (its value, start pos [X;Y], length)) for row X
#   [X] 3) in 2D array => create list of possible gears * (start pos [X;Y], [array of numbers])) for row X
#   [X] 4) go through parts => check if star x,y is within min,max x,y of part and add it, if is
#   [X] 5) sum values of numbers, of those stars which contain exactly 2 obj's in star's [array of numbers]

# Variables
#FILE_NAME = "input.small.txt"
FILE_NAME = "input.txt"


class NumberInSchematic:
    def __init__(self, x, y):
        self.IsPartNumber = False        # by default
        self.ind_row = x
        self.ind_col = y
    
    def FinishObject(self, value, length):
        self.Value = value
        self.length = length

    # in order to work with print function for example
    def __str__(self):
        return f"{self.Value} | [x;y] {self.ind_row}; {self.ind_col} | Len: {self.length} | PartNumber: {self.IsPartNumber}"

    # in order to compare various objects
    def __eq__(self, other):
        if (self.Value == other.Value and self.ind_row == other.ind_row and self.ind_col == other.ind_col):
            return True
        
        return False

# Functions
## 
def Get2DArrayAndDimensionsFromFile(file):
    tmpArr = []
    file.seek(0, 0)
    
    # make 2D array out of each line, get rid of \r\n
    tmpArr = [list(line.strip()) for line in file]
    
    # assuming the rows are of the same length
    return tmpArr, len(tmpArr), len(tmpArr[0])


## Go through the line and use state-wise approach to identify if next char is also number
def GetAllNumberObjectsFromLine(line, rowIndex):
    # print(line)
    
    tmpList = []

    # constantly rewritten attributes to remember stats over and after for cycle
    objInGen    = None
    build_Num   = ""

    for y in range(0, len(line)):
        curr_Char = line[y]
        isNumeric = curr_Char.isnumeric()

        # Current char is Numeric
        if isNumeric:
            if (objInGen is None):
                objInGen = NumberInSchematic(rowIndex, y)
                build_Num = ""

            build_Num += curr_Char
            
        # Current char is Non-Numeric
        if isNumeric == False:
            
            if (objInGen is None):
                continue

            ## if we have some number in generation

            objInGen.FinishObject(int(build_Num), len(build_Num))
            # print(f"Creating object with stats: {objInGen}")
            tmpList.append(objInGen)
            
            # prepare in case of next number will come
            objInGen = None
    
    
    # after for cycle is finished, its necessary to test whether we were not in process
    # of some number generation, add it now if yes
    if (objInGen is not None):
        objInGen.FinishObject(int(build_Num), len(build_Num))
        tmpList.append(objInGen)

    return tmpList

## Go through the line and use state-wise approach to identify if next char is also number
def GetAllStarPositionsFrom2DArray(arr):
    tmpArr = []
    
    for x in range(0, len(arr)):
        for y in range(0, len(arr[x])):
            currChar = arr[x][y]
            
            if (currChar == '*'):
                tmpArr.append([x, y, []])

    return tmpArr

def GetMinCoordsForNumInArray(num):
    min_x = num.ind_row - 1
    min_y = num.ind_col - 1

    # check if boundaries are legit
    if (min_x < 0):
        min_x = 0
    
    if (min_y < 0):
        min_y = 0

    return min_x, min_y

def GetMaxCoordsForNumInArray(num, arr):
    max_x = num.ind_row + + 1
    max_y = num.ind_col + num.length

    # check if boundaries are legit
    if (max_x >= len(arr)):
        max_x -= 1
    
    if (max_y >= len(arr[0])):
        max_y -= 1

    return max_x, max_y

def GoAroundNumberInArrayAndFindIfHasPartIdentifierChar(arr, num):
    # set default boundaries to check
    min_x, min_y = GetMinCoordsForNumInArray(num)
    max_x, max_y = GetMaxCoordsForNumInArray(num, arr)
       
    # go through all combinations of x,y from min -> max
    # e.g.: number 4 is at position 3,3 and check above her is at index 2,2; 2,3; 2,4 (so we need 3 numbers for Y and 4-2 is 2. To get 3 is + 1)
    x_arr = np.linspace(min_x, max_x, (max_x - min_x + 1), dtype=int)
    y_arr = np.linspace(min_y, max_y, (max_y - min_y + 1), dtype=int)

    # go through the 2D scheme array and check positions of x_arr and y_arr
    # to make it readable we go through the list by columns first
    for x in x_arr:
        for y in y_arr:
            checked_char = arr[x][y]
            # if it's numeric   => ignore
            if (checked_char.isnumeric()):
                continue

            # if it's '.'       => ignore
            if (checked_char == '.'):
                continue

            # if it's sth else  => part number
            return True
    
    return False

def GoAroundPartsInArrayAndFindAllStarsAround(scheme, partArr, starArr):
    # For each Number in NumArr
    for part in partArr:
        # set default boundaries to check
        min_x, min_y = GetMinCoordsForNumInArray(part)
        max_x, max_y = GetMaxCoordsForNumInArray(part, scheme)

        # star [x_star, y_star, List<part>]
        for star in starArr:
            if (star[0] >= min_x and star[0] <= max_x and star[1] >= min_y and star[1] <= max_y):
                star[2].append(part)


## part I
def SumNumbersOfParts():
    ## Go through the object list and mark the parts (count as well)
    sumOfAll = 0
    for numObj in num_list:
        # print(numObj)

        # Find out if there is a Non-Digit, Non-'.' char around the object
        numObj.IsPartNumber = GoAroundNumberInArrayAndFindIfHasPartIdentifierChar(scheme, numObj)
        
        # Sum after we know
        if (numObj.IsPartNumber):
            sumOfAll += numObj.Value

    print(f"The sum of all of the part numbers is {sumOfAll}")

## part II 
# Gear-Ratio is a multiplication of two adjacent numbers next to '*' (exactly 2 adjacency)
def SumGearRatiosOfGears(star_list):
    sumOfAll = 0

    for star in star_list:
        if (len(star[2]) == 2):
            sumOfAll += star[2][0].Value * star[2][1].Value
        
    print(f"The sum of all of the gear ratios is {sumOfAll}")

############## INITIAL CODE ############
if __name__ == "__main__":
    
    file = open(FILE_NAME, 'r')
    
    ## Get the engine scheme into 2D array + its dimensions
    scheme, row_count, col_count = Get2DArrayAndDimensionsFromFile(file)

    ## Debug info
    # print(scheme)
    # print(f"Matrix has dimensions of {row_count}x{col_count}")

    ## Go through the array and make the object list
    num_list = []
    for line_number in range (0, row_count):
        ## Add returned list of objects to already existing list
        num_list += GetAllNumberObjectsFromLine(scheme[line_number], line_number)

    ############ part 1 ###########
    # also influences the num_list which overrides IsPartNumber for each instance
    SumNumbersOfParts()

    ############ part 2 ###########
    # Just add only those numbers which are parts
    part_list = []
    for num in num_list:
        if (num.IsPartNumber):
            part_list.append(num)
            print(num)


    # Create a list of '*'  [x_star, y_star, List<part>]
    star_list = GetAllStarPositionsFrom2DArray(scheme)

    # Gear is only that part which is adjacent to another part via '*'    
    GoAroundPartsInArrayAndFindAllStarsAround(scheme, part_list, star_list)
    
    # First remove parts that are not parts, 
    SumGearRatiosOfGears(star_list)