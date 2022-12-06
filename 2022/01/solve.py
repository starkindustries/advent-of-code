
elves = []

filename = "input.txt"
with open(filename, 'r') as handle:
    calories = 0
    for line in handle:        
        line = line.strip()
        try:            
            calories += int(line)
        except Exception as e:
            elves.append(calories)
            calories = 0
elves.append(calories)

elves.sort(reverse=True)
maxcals = elves[0] + elves[1] + elves[2]
print("Max elf calories: ", maxcals)
