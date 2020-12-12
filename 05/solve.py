
# 0123 4567
# 0000 0000
# RRR
def getSeatID(seatCode):
    seatRow = seatCode[0:7]
    seatCol = seatCode[7:]
    
    rowLeftIndex, rowRightIndex = 0, 128
    colLeftIndex, colRightIndex = 0, 8
    print(seatRow)
    for letter in seatRow:
        if letter == "F":
            rowRightIndex = (rowLeftIndex + rowRightIndex) // 2
        else:
            rowLeftIndex = (rowLeftIndex + rowRightIndex) // 2
        row = (rowLeftIndex + rowRightIndex) // 2

    print(seatCol)
    for letter in seatCol:
        if letter == "L":
            colRightIndex = (colLeftIndex + colRightIndex) // 2
        else:
            colLeftIndex = (colLeftIndex + colRightIndex) // 2
        col = (colRightIndex + colLeftIndex) // 2
    print(f"Row: {rowLeftIndex},{rowRightIndex}. Col: {colLeftIndex},{colRightIndex}")
    print(f"row, col: {row}, {col}")
    return row * 8 + col

maxSeatID = -1
seatList = []
with open("input.txt", 'r') as handle:
    for line in handle:        
        seatCode = line.strip()
        print(seatCode)
        seatID = getSeatID(seatCode)
        maxSeatID = max(maxSeatID, seatID)
        seatList.append(seatID)
print(f"highest seat ID: {maxSeatID}")
print(f"seats: {sorted(seatList)}")

# part 2
seatList.sort()
for i in range(len(seatList) - 1):
    if seatList[i + 1] - seatList[i] > 1:
        print(f"Your seat: {seatList[i] + 1}")
        break
