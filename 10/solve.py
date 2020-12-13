
filename = "input.txt"
# filename = "sample2.txt"

adapters = []
with open(filename, "r") as handle:    
    for line in handle:
        number = int(line.strip())
        adapters.append(number)

adapters.append(0)
adapters.sort()
deviceJolts = adapters[len(adapters)-1] + 3
adapters.append(deviceJolts)

diffCount = {}
for i in range(len(adapters)-1):
    diff = adapters[i+1] - adapters[i]
    diffCount[diff] = diffCount.get(diff, 0) + 1

# Part 1
print(diffCount)
print(f"1-jolt * 3-jolt diffs: {diffCount[1] * diffCount[3]}")