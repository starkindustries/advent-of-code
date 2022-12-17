#!/usr/bin/python3.7
# day4

import sys
import datetime
import copy

# Main Program
if __name__ == "__main__":
    filename = str(sys.argv[1])
    print("Filename: {}".format(filename))

fileObject = open(filename, "r")
lines = fileObject.read().splitlines()

polymer = str(lines[0])
# print(lines[0])

alphabet = "abcdefghijklmnopqrstuvwxyz"


def reactPolymer(polymer):
    didChange = True
    while didChange:
        didChange = False
        for i in range(26):
            t1 = alphabet[i].upper() + alphabet[i]
            t2 = alphabet[i] + alphabet[i].upper()
            # print("{} {}".format(t1, t2))

            lenBefore = len(polymer)
            polymer = polymer.replace(t1, "")
            polymer = polymer.replace(t2, "")
            if len(polymer) < lenBefore:
                # change occurred
                didChange = True
    return polymer


length = len(reactPolymer(polymer))
print("Part 1: Polymer length: {}".format(length))

polyLengths = []
for i in range(26):
    temp = polymer
    temp = temp.replace(alphabet[i], "")
    temp = temp.replace(alphabet[i].upper(), "")
    temp = reactPolymer(temp)
    polyLengths.append(len(temp))

length = min(polyLengths)
print("Part 2: Min polymer length: {}".format(length))
