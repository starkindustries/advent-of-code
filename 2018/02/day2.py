#!/usr/bin/python3.5

import sys

filename = "input.txt"
fileObject = open(filename, "r")
boxIds = fileObject.read().splitlines()

doubleCount = 0
tripleCount = 0

for boxId in boxIds:
    # create a dictionary with this format:
    # {'letter': 'number of occurences in ID'}
    dictionary = {}
    for char in boxId:
        if char in dictionary:
            dictionary[char] += 1
        else:
            dictionary[char] = 1
    if 2 in dictionary.values():
        doubleCount += 1
    if 3 in dictionary.values():
        tripleCount += 1

checksum = doubleCount * tripleCount
print("Part 1. Checksum: ", checksum)

print("Part 2. Find boxes that differ by just one character.")


def doesDiffByOneCharacter(a, b):
    diffCount = 0
    differentCharIndex = -1
    for i in range(0, len(a), 1):
        if a[i] != b[i]:
            diffCount += 1
            differentCharIndex = i
        if diffCount > 1:
            # To write a tuple containing a single value you have to include a comma,
            # even though there is only one value:
            return (False,)
    # https://www.tutorialspoint.com/python/python_tuples.htm
    return (True, differentCharIndex)


start = 0
stop = len(boxIds)-1  # stop at the second to last item
step = 1
# Classic for-loop in python:
for i in range(start, stop, step):
    # start from the item after i
    # end at the last item in array
    for j in range(i+1, stop+1, step):
        boxA = boxIds[i]
        boxB = boxIds[j]
        # print("Comparing: {} and {}".format(boxA, boxB))
        result = doesDiffByOneCharacter(boxA, boxB)
        if result[0]:  # result[0] is a boolean
            diffIndex = result[1]
            print("[{}] and [{}] differ by one char at index {}.".format(
                boxA, boxB, diffIndex))
            print("_BoxA: {}".format(boxA))
            print("_BoxB: {}".format(boxB))
            print("Share: {} {}".format(boxA[:diffIndex], boxA[diffIndex+1:]))
            print("PART2 ANSWER: {}{}".format(
                boxA[:diffIndex], boxA[diffIndex+1:]))
            break
