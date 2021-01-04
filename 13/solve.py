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
#                 1    1    2    2    3    3    4    4    5    5    6    6    7    7    8
# time : ----5----0----5----0----5----0----5----0----5----0----5----0----5----0----5----0
# bus 3: --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
# bus 5: ----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
# bus 7: ------*------*------*------*------*------*------*------*------*------*------*------*------*------*

# For buses 3 and 5, the first instance of a valid timestamp is 9, followed by 24, then 39.
# 9, 24, 39 growing linearly by 15. 15 is the product of 3 and 5 (the two buses).
# Now add bus 7 into this calculation, continuing to increase the timestamp by 15 at each check.
# The first valid timestamp for 3, 5, and 7 is at 54. 
# Then the next valid timestamp would be at 54 + (3 * 5 * 7) = 54 + 105 = 159

def findTimestamp(input):
    buses = [bus for bus in input.split(",")]    
    multiple = int(buses[0])
    t = multiple
    for i in range(1, len(buses)):
        try:
            bus = int(buses[i])
        except:
            # this will happen if bus is "x"
            continue
        while True:            
            if ((t + i) / int(bus)).is_integer():                
                multiple *= bus
                break
            t += multiple
    print(f"Found t[{t}] for input {input}")
    return t

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

offsets, _ , _ = calculateOffsets("3,5")
assert checkTimestamp(10, offsets) == True
assert findTimestamp("3,7") == 6
assert findTimestamp("3,5,7") == 54

# Solve part 2
DEBUG = True
print(f"{fileInput[1]}")
findTimestamp(fileInput[1])