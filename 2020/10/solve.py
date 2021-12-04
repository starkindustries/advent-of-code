#!/usr/bin/python3

filename = "input.txt"
# filename = "sample.txt"

adapters = []
with open(filename, "r") as handle:
    for line in handle:
        number = int(line.strip())
        adapters.append(number)

adapters.append(0)
adapters.sort()
deviceJolts = adapters[len(adapters)-1] + 3
adapters.append(deviceJolts)

# part 1
diffCount = {}

# part 2
# See "Gaps to Combos" section below
gapsToCombos = {2: 2, 3: 4, 4: 7}
last3DiffIndex = 0
numCombos = 1

for i in range(len(adapters)-1):
    # For part 1
    diff = adapters[i+1] - adapters[i]
    diffCount[diff] = diffCount.get(diff, 0) + 1

    # For part 2
    if diff == 3:
        # Calculate the 1-gap length
        oneGap = i - last3DiffIndex
        # If 1-gap is greater than 1, multiple combos are possible
        if oneGap > 1:
            try:
                numCombos *= gapsToCombos[oneGap]
            except:
                print(
                    f"Error: no key found in gapsToCombos for 1-gap of: {oneGap}")
                print(f"gapsToCombos: {gapsToCombos}")
                exit()
        # Update the last 3-diff index
        last3DiffIndex = i + 1

# Part 1
print(diffCount)
print(f"Part 1: 1-jolt * 3-jolt diffs: {diffCount[1] * diffCount[3]}")

# Part 2
print(f"Part 2: number of combos {numCombos}")

# *************************
# Gaps to Combos
# *************************
# For the first gap of given input {0, 1, 2, 3, 4}, both 0 and 4 are required.
# 0 _ 4: one space. 3 options for slot 1: adapters 1, 2, or 3
# 0 _ _ 4: two spaces. 3 options: adapters (1, 2), (1, 3), (2, 3)
# 0 _ _ _ 4: three spaces. 1 option.
# Total of 7 possible combos for 1-gap of 4

# What about 1-gap of 3, e.g. {5, 6, 7, 8}
# 5 8: this is an option.
# 5 _ 8: two options: adapters 6 or 7
# 5 6 7 8: also an option
# Total of 4 possible combos for 1-gap of 3

# 1-gap of 2, e.g. {5, 6, 7}
# {5, 7} and {5, 6, 7}
# Total of 2 combos for 1-gap of 2
