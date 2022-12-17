#!/usr/bin/python3.7

import sys
import datetime
import copy

# Function Definitions
def printMap(tempMap):
    for line in tempMap:
        print("".join(line))


# Main Program
if __name__ == "__main__":
    filename = str(sys.argv[1])
    print("Filename: {}".format(filename))

isDebugging = filename == "input2.txt"

# Read the file and split input by new lines
fileObject = open(filename, "r")
lines = fileObject.read().splitlines()

# ==========================================
print("PART 1")

# For each line in lines, split line into a tuple(x, y)
locations = list(
    map(lambda line: tuple(map(lambda coord: int(coord), line.split(", "))), lines)
)
print("Locations: {}".format(locations))

# Count the number of locations
numLocations = len(locations)
print("Number of locations: {}".format(numLocations))

# Get the max boundaries of the map
xMax = max(locations, key=lambda coord: coord[0])[0] + 2
yMax = max(locations, key=lambda coord: coord[1])[1] + 1
print("Max XY: [{}, {}]".format(xMax, yMax))

# Initialize the map with dashes
myMap = [["-" for x in range(xMax)] for y in range(yMax)]

if isDebugging:
    # Set the locations in the map with the index: 0 thru numLocations
    for index, coord in enumerate(locations):
        # Note: locations has format [x,y] and myMap is myMap[y][x]:
        myMap[coord[1]][coord[0]] = str(index)
    print("My Map:")
    printMap(myMap)  # Check that everything looks good so far

# loop through the entire map
for y in range(yMax):
    for x in range(xMax):
        # Get (x,y)'s distance from all locations and find the minimum distance
        distances = list(
            map(lambda coord: abs(y - coord[1]) + abs(x - coord[0]), locations)
        )
        minDistance = min(distances)
        # From the list of distances, get only the min distances
        matches = [dist for dist in distances if dist == minDistance]
        if len(matches) == 1:  # if length is 1, only one location is closest
            myMap[y][x] = str(distances.index(minDistance))
        else:  # if length is greater than 1, two or more locations are equally close
            myMap[y][x] = "."
if isDebugging:
    print("Map Checkpoint:")
    printMap(myMap)  # Check that map matches example

# Get the map's perimeter. Those on the perimeter expand infinitely
edges = myMap[0].copy()  # top edge
edges.extend(myMap[yMax - 1])  # bottom edge
edges.extend([x[0] for x in myMap])  # left edge
edges.extend([x[xMax - 1] for x in myMap])  # right edge
infiniteLocations = list(set(edges))  # get unique values
# Verify that these are the infinite locations
print("Infinite locations: {}".format(infiniteLocations))

# Find the finite locations
locationIndexes = [str(x) for x in range(numLocations)]
finiteLocations = [x for x in locationIndexes if x not in infiniteLocations]
# Verify these are the finite locations
print("Finite locations: {}".format(finiteLocations))

areas = []
for location in finiteLocations:
    # Get the sum of all occurences of location e.g. '0', '1', etc.
    areas.append(sum(x.count(location) for x in myMap))

print("Areas: {}".format(areas))
print("Max area: {}".format(max(areas)))
print("")

# ==========================================
print("PART 2")

# Set the 'within' distance depending on the filename
if isDebugging:
    partTwoDistance = 32
else:
    partTwoDistance = 10000

for y in range(yMax):
    for x in range(xMax):
        # for each coord(x,y) get a list of all distances from coord to all locations
        distances = list(
            map(lambda coord: abs(y - coord[1]) + abs(x - coord[0]), locations)
        )
        # if the sum of those distances is less than the requirement then it is "within the desired region"
        if sum(distances) < partTwoDistance:
            myMap[y][x] = "#"
if isDebugging:
    print("Map Checkpoint:")
    printMap(myMap)
area = sum(x.count("#") for x in myMap)
print("Area: {}".format(area))
