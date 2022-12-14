#!/usr/bin/python3.5
# day3

import sys

# Main Program
if __name__ == "__main__":
    filename = str(sys.argv[1])
    print("Filename: {}". format(filename))

fileObject  = open(filename, "r")
fabricData = fileObject.read().splitlines()

# . dot is unclaimed fabric
# 1 is claimed fabric by claimId 1
# X is intersecting fabric
fabricW = 1000
fabricH = 1000

# initialize fabric with dots
fabric = [["." for i in range(fabricW)] for j in range(fabricH)]

def printFabric():
    for line in fabric:
        for square in line:
            print(square, end='  ')
        print()

# printFabric()
# print("==========================")

# This array will hold: [claimId, fromLeft, fromTop, width, height]
fabricDataArray = []

# Build the fabric intersection table
for data in fabricData:
    temp = data.split('@')   
    claimId = int(temp[0].split('#')[1])    
    
    temp = temp[1].split(':')
    
    # fromLeft and fromTop margins
    margins = temp[0]
    margins = margins.split(',')
    fromLeft = int(margins[0])
    fromTop = int(margins[1])

    # width and height
    widthHeight = temp[1]
    widthHeight = widthHeight.split('x')
    width = int(widthHeight[0])
    height = int(widthHeight[1])
    # print("{},{} and {}x{}".format(fromLeft, fromTop, width, height))

    fabricDataArray.append([claimId, fromLeft, fromTop, width, height])    

    for i in range(0, height, 1):
        for j in range(0, width, 1):
            square = fabric[i+fromTop][j+fromLeft]            
            if square == '.':
                fabric[i+fromTop][j+fromLeft] = claimId
            else:
                fabric[i+fromTop][j+fromLeft] = 'X'
        
# printFabric()

# Find the claimID with no intersections
def findClaimWithNoIntersections():
    for data in fabricDataArray:
        claimId  = data[0]
        fromLeft = data[1]
        fromTop  = data[2]
        width    = data[3]
        height   = data[4]

        isIntersected = False
        for i in range(0, height, 1):
            for j in range(0, width, 1):
                if fabric[i+fromTop][j+fromLeft] == '.':
                    print("ERROR")
                elif fabric[i+fromTop][j+fromLeft] == 'X':
                    isIntersected = True
                elif int(fabric[i+fromTop][j+fromLeft]) == claimId:
                    pass
                else:
                    print("ERROR")
        
        if isIntersected:
            pass
        else:
            print("Non-Intersecting Claim ID: {}".format(claimId))
            break

# Count number of intersecting fabric claims
def countNumIntersections():
    intersectionCount = 0
    for i in range(0, fabricH, 1):
        for j in range(0, fabricW, 1):
            if fabric[i][j] == 'X':
                intersectionCount += 1
    print("Number of Intersections: {}".format(intersectionCount))

countNumIntersections()
findClaimWithNoIntersections()    

    