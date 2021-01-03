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
diff3Indices = []

for i in range(len(adapters)-1):
    # For part 1    
    diff = adapters[i+1] - adapters[i]
    diffCount[diff] = diffCount.get(diff, 0) + 1
    # For part 2
    if diff == 3:
        # add both indices to the tracker
        diff3Indices.extend([i, i+1])

# Part 1
print(diffCount)
print(f"Part 1: 1-jolt * 3-jolt diffs: {diffCount[1] * diffCount[3]}")

# Part 2
print("adapters")
print(adapters)
print("diff3indices")
print(diff3Indices)
# Account for the 1-gap from 0 volts to the first 3-volt difference
gapTracker = [diff3Indices[0]]
# Find differences in indices greater than 1
for i in range(len(diff3Indices)-1):
    gap = diff3Indices[i+1] - diff3Indices[i]
    if gap > 1:
        gapTracker.append(gap)

print("gap tracker")
print(gapTracker)
print(max(gapTracker))

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
gapsToCombos = { 0 : 0, 1: 0, 2: 2, 3:4, 4:7 }
numCombos = 1
for gap in gapTracker:
    numCombos *= gapsToCombos[gap]

print(f"combos: {numCombos}")