
import pytest

DEBUG = True

# Pre-compute the powers of 2's
twosPlaces = [2**x for x in range(35, -1, -1)]
# print(twosPlaces)

def convertDecimalToBinary(n):
    temp = n
    binary = ""
    for place in twosPlaces:
        if temp >= place:
            binary += "1"
            temp -= place
        else:
            binary += "0"
    if DEBUG:
        print(f"Decimal {n} converts to binary {binary}")
    return binary

assert convertDecimalToBinary(11)  == "000000000000000000000000000000001011"
assert convertDecimalToBinary(73)  == "000000000000000000000000000001001001"
assert convertDecimalToBinary(101) == "000000000000000000000000000001100101"
assert convertDecimalToBinary(64)  == "000000000000000000000000000001000000"
assert convertDecimalToBinary(0)   == "000000000000000000000000000000000000"

def convertBinaryToDecimal(n):
    result = 0
    for i, bit in enumerate(n):        
        result += int(bit) * twosPlaces[i]
    if DEBUG:
        print(f"Binary {n} converts to decimal {result}")
    return result

assert convertBinaryToDecimal("000000000000000000000000000000001011") == 11
assert convertBinaryToDecimal("000000000000000000000000000001001001") == 73
assert convertBinaryToDecimal("000000000000000000000000000001100101") == 101
assert convertBinaryToDecimal("000000000000000000000000000001000000") == 64
assert convertBinaryToDecimal("000000000000000000000000000000000000") == 0

def applyBitmask(decimal, mask):
    binary = convertDecimalToBinary(decimal)
    result = ""
    for maskbit, value in zip(mask, binary):
        if maskbit == "X":
            result += value
        elif maskbit == "1":
            result += "1"
        elif maskbit == "0":
            result += "0"
        else:
            print(f"ERROR: unexpected value in mask: {mask}")
    return convertBinaryToDecimal(result)

assert applyBitmask(11, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == 73
assert applyBitmask(101, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == 101
assert applyBitmask(0, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == 64

# ******************
# Part 1
# ******************

filename = "input.txt"
# filename = "sample.txt"

with open(filename, 'r') as handle:
    program = [line.strip() for line in handle]
print(program)

# Run program
memory = {}
mask = ""
for line in program:
    line = line.split(" ")    
    if line[0] == "mask":
        # update mask
        mask = line[2]
    else:
        # execute mem instruction
        address = int(line[0][4:-1])
        value = int(line[2])
        memory[address] = applyBitmask(value, mask)

# Program completed
print(memory)
resultSum = 0
for _, value in memory.items():
    resultSum += value
print(f"Part 1 sum: {resultSum}")