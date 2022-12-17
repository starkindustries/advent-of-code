filename = "sample.txt"
filename = "input.txt"

seatMap = []
with open(filename, "r") as handle:
    for line in handle:
        line = line.strip()
        seatMap.append(line)


def occupiedAdjacentSeats(row, col, seatMap):
    occupied = 0
    # row above
    if row > 0:
        # directly above
        if seatMap[row - 1][col] == "#":
            occupied += 1
        # diag: above, left
        if col > 0:
            if seatMap[row - 1][col - 1] == "#":
                occupied += 1
        # diag: above, right
        if col < len(seatMap[0]) - 1:
            if seatMap[row - 1][col + 1] == "#":
                occupied += 1
    # row below
    if row < len(seatMap) - 1:
        # directly below
        if seatMap[row + 1][col] == "#":
            occupied += 1
        # diag: below, left
        if col > 0:
            if seatMap[row + 1][col - 1] == "#":
                occupied += 1
        # diag: below, right
        if col < len(seatMap[0]) - 1:
            if seatMap[row + 1][col + 1] == "#":
                occupied += 1
    # col left
    if col > 0:
        # directly left
        if seatMap[row][col - 1] == "#":
            occupied += 1
    # col right
    if col < len(seatMap[0]) - 1:
        # directly right
        if seatMap[row][col + 1] == "#":
            occupied += 1
    return occupied


def countOccupiedSeats(seatMap):
    count = 0
    for row in seatMap:
        count += row.count("#")
    return count


def applyRules(seatMap):
    newMap = []
    for i in range(len(seatMap)):
        newRow = ""
        for j in range(len(seatMap[0])):
            # row, col = i, j
            seat = seatMap[i][j]
            occupied = occupiedAdjacentSeats(i, j, seatMap)
            if seat == "L" and occupied == 0:
                newRow += "#"
            elif seat == "#" and occupied >= 4:
                newRow += "L"
            elif seat == ".":
                newRow += "."
            else:
                newRow += seat
        newMap.append(newRow)
    return newMap


def stateChanged(map1, map2):
    for r1, r2 in zip(map1, map2):
        if r1 != r2:
            return True
    return False


def printMap(myMap):
    for line in myMap:
        print(line)


map1 = seatMap
map2 = applyRules(seatMap)
while stateChanged(map1, map2):
    map1 = map2
    map2 = applyRules(map1)
    # print("m1:")
    # printMap(map1)
    # print("m2:")
    # printMap(map2)
count = countOccupiedSeats(map1)
print(f"Seating stabilized! Occupied seats: {count}")
