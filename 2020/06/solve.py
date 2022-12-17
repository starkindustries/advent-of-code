def processAnswers(input, group):
    # input is one person's answers
    # group is the set of 'yes' answers
    for letter in input:
        group.add(letter)


yesTotal = 0
with open("input.txt", "r") as handle:
    group = set()
    for line in handle:
        line = line.strip()
        if line == "":
            yesTotal += len(group)
            # print(f"group count: {len(group)}")
            group = set()
        else:
            processAnswers(line, group)
    # process last line
    processAnswers(line, group)
    yesTotal += len(group)

print(f"Yes count: {yesTotal}")

# part 2


def processEveryoneYes(input, group):
    for letter in input:
        group[letter] = group.get(letter, 0) + 1


def getYesCount(group, groupCount):
    total = 0
    for _, value in group.items():
        if value == groupCount:
            total += 1
    # print(f"g, gc, total: {group}, {groupCount}, {total}")
    return total


yesTotal = 0
with open("input.txt", "r") as handle:
    group = {}
    groupCount = 0
    for line in handle:
        line = line.strip()
        if line == "":
            yesTotal += getYesCount(group, groupCount)
            group = {}
            groupCount = 0
        else:
            processEveryoneYes(line, group)
            groupCount += 1
    # process last line
    yesTotal += getYesCount(group, groupCount)
print(f"Everyone yes: {yesTotal}")
