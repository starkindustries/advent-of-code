#!/usr/bin/python3

import math
import pytest

DEBUG = True

filename = "input.txt"
# filename = "sample.txt"

# sample input
# 939
# 7,13,x,x,59,x,31,19

with open(filename, 'r') as handle:
    fileInput = [line.strip() for line in handle]

departureTime = int(fileInput[0])
buses = [bus for bus in fileInput[1].split(",")]

print(departureTime)
print(buses)

minWaitTime = math.inf
busID = -1

for bus in buses:
    if bus == "x":
        continue
    bus = int(bus)
    factor = math.ceil(departureTime / bus)
    print(f"{departureTime} / {bus} = {factor}")
    closestTime = factor * bus
    waitTime = closestTime - departureTime
    if waitTime < minWaitTime:
        minWaitTime = waitTime
        busID = bus

print(
    f"Part 1: Wait {minWaitTime} minutes for bus {busID} = {minWaitTime * busID}")

# Part 2
def calculateOffsets(input):
    buses = [bus for bus in input.split(",")]

    # Strategy: get the largest bus ID and use that as the check point for all other buses
    # This will reduce having to check all timestamps by a factor of the bus's ID number
    maxBusID = max([int(bus) for bus in buses if bus != "x"])
    maxIndex = buses.index(str(maxBusID))
    if DEBUG:
        print(f"Max bus ID [{maxBusID}] at index {maxIndex}")

    # Get offset pairs (ID, offset) for all buses
    offsets = []
    for i in range(len(buses)):
        bus = buses[i]
        if bus == "x":
            continue
        offset = (int(bus), i - maxIndex)
        offsets.append(offset)    
    # sort offset by max ID
    offsets = sorted(offsets, key = lambda tup: tup[0], reverse=True)
    # Remove max offset pair; not needed
    offsets.pop(0)
    if DEBUG:
        print(f"Offset list: {offsets}")
    return offsets, maxBusID, maxIndex

def checkTimestamp(t, offsets):
    for bus, offset in offsets:
        if not ( (t + offset) / bus ).is_integer():
            # print(f"Not integer: {t}, {offset}, {bus} = {t + offset / bus}")
            return False
    return True

def findTimestamp(input):    
    t = 0
    offsets, maxBusID, maxIndex = calculateOffsets(input)    

    while True:
        if checkTimestamp(t, offsets):
            # Adjust timestamp by the index of max bus ID
            if DEBUG:
                print(f"Found earliest valid timestamp at: {t - maxIndex}")
            return t - maxIndex
        t += maxBusID
        # print(f"t: {t}")

# Initial test
offsets, _ , _ = calculateOffsets("7,13,x,x,59,x,31,19")
assert checkTimestamp(0, offsets) == False
assert checkTimestamp(1068785, offsets) == True

# Tests from problem description
assert findTimestamp("7,13,x,x,59,x,31,19") == 1068781
assert findTimestamp("17,x,13,19") == 3417
assert findTimestamp("67,7,59,61") == 754018
assert findTimestamp("67,x,7,59,61") == 779210
assert findTimestamp("67,7,x,59,61") == 1261476
assert findTimestamp("1789,37,47,1889") == 1202161486

# Solve part 2
# DEBUG = True
# print(f"{fileInput[1]}")
# findTimestamp(fileInput[1])

# t / 7 % 1 == 0
# (t + 7) / 19 % 1 == 0
# 19 * x = t + 7
# 7 * y = t