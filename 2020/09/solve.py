preambleLength = 5
inputFile = "sample.txt"

preambleLength = 25
inputFile = "input.txt"

xmasData = []
with open(inputFile, "r") as handle:
    for line in handle:
        number = int(line.strip())
        xmasData.append(number)

# print(xmasData)

# Populate 'previous' numbers array
previous = []
for i in range(preambleLength):
    previous.append(xmasData[i])

# Loop through the numbers following the preamble
# Take the number subtract it by each value in the 'previous' array.
# If the difference is in 'previous' AND is not the same number
# ("the two numbers in the pair must be different")
# then it is a valid number
invalidNumber = -1
for i in range(preambleLength, len(xmasData)):
    valid = False
    for number in previous:
        diff = xmasData[i] - number
        if diff in previous and diff != number:
            # print(f"Valid number found: {number} + {diff} = {xmasData[i]}")
            valid = True
            break
        # else continue searching
    if not valid:
        invalidNumber = xmasData[i]
        print(f"Found invalid number: {invalidNumber}")
        break

    # Update previous array
    previous.append(xmasData[i])
    previous.pop(0)

# Part 2
for i in range(len(xmasData)):
    j = 0
    contiguousSum = 0
    while contiguousSum < invalidNumber and (i + j) < len(xmasData):
        contiguousSum += xmasData[i + j]
        if contiguousSum == invalidNumber:
            contiguousSet = xmasData[i : i + j + 1]
            print("Found contiguous set!")
            print(contiguousSet)
            print(f"Encryption weakness: {min(contiguousSet) + max(contiguousSet)}")
            exit()
        j += 1
