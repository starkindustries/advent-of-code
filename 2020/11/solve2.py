filename = "sample.txt"
filename = "input.txt"

seatMap = []
with open(filename, "r") as handle:
    for line in handle:
        line = line.strip()
        seatMap.append(line)

height = len(seatMap)
width = len(seatMap[0])


def checkSeatHelper(seatMap, row, col, i, occupied):
    seat = seatMap[row][col]
    if seat == ".":
        return (False, i + 1, occupied)
    elif seat == "#":
        return (True, 0, occupied + 1)
    elif seat == "L":
        return (True, 0, occupied)


def occupiedAdjacentSeats(row, col, seatMap):
    occupied = 0
    # directly above
    i, seatFound = 1, False
    while row - i >= 0 and not seatFound:
        seatFound, i, occupied = checkSeatHelper(seatMap, row - i, col, i, occupied)
    # diag: above, left
    i, seatFound = 1, False
    while row - i >= 0 and col - i >= 0 and not seatFound:
        seatFound, i, occupied = checkSeatHelper(seatMap, row - i, col - i, i, occupied)
    # diag: above, right
    i, seatFound = 1, False
    while row - i >= 0 and col + i < width and not seatFound:
        seatFound, i, occupied = checkSeatHelper(seatMap, row - i, col + i, i, occupied)
    # directly left
    i, seatFound = 1, False
    while col - i >= 0 and not seatFound:
        seatFound, i, occupied = checkSeatHelper(seatMap, row, col - i, i, occupied)
    # directly right
    i, seatFound = 1, False
    while col + i < width and not seatFound:
        seatFound, i, occupied = checkSeatHelper(seatMap, row, col + i, i, occupied)
    # directly below
    i, seatFound = 1, False
    while row + i < height and not seatFound:
        seatFound, i, occupied = checkSeatHelper(seatMap, row + i, col, i, occupied)
    # diag: below, left
    i, seatFound = 1, False
    while row + i < height and col - i >= 0 and not seatFound:
        seatFound, i, occupied = checkSeatHelper(seatMap, row + i, col - i, i, occupied)
    # diag: below, right
    i, seatFound = 1, False
    while row + i < height and col + i < width and not seatFound:
        seatFound, i, occupied = checkSeatHelper(seatMap, row + i, col + i, i, occupied)
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
            elif seat == "#" and occupied >= 5:
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
count = countOccupiedSeats(map1)
print(f"Seating stabilized! Occupied seats: {count}")
