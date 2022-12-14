#!/usr/bin/python3.5

import sys

filename = "input.txt"
fileObject  = open(filename, "r")

changeArray = fileObject.read().splitlines()

frequency = 0

print("PART 1")
for change in changeArray:
    sign = change[0]
    
    if sign == '+':
        frequency += int(change[1:])
    elif sign == '-':
        frequency -= int(change[1:])

print("Final frequency: " + str(frequency))

print("PART 2")
frequency = 0
freqArray = [0]
duplicateFound = False
numTimesLooped = 0

print("First duplicate: 390")
print("Array length: 138573")
print("Number of times looped through input: 137")

while not duplicateFound:
    for change in changeArray:
        sign = change[0]
        
        if sign == '+':
            frequency += int(change[1:])
        elif sign == '-':
            frequency -= int(change[1:])
                
        message = "[{}, {}, {}]".format(frequency, len(freqArray), numTimesLooped)
        sys.stdout.write("\r"+message)
        sys.stdout.flush()

        if frequency in freqArray:
            print("Match found [freq, #list-items, #loops]: " + message)
            duplicateFound = True
            break
        freqArray.append(frequency)

    numTimesLooped += 1



