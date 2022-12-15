import re
import functools

def solve():
    pass


def parse_coords(line):
    line = line.split(", ")
    x = int(line[0][2:])
    y = int(line[1][2:])
    return (x, y)


sensorlist = []

maxrow = 4000000
row = 2000000
filename = "input.txt"

# maxrow = 20
# row = 10
# filename = "sample.txt"

with open(filename, 'r', encoding='utf8') as handle:    
    for line in handle:

        # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        # https://pythex.org/
        result = re.findall(r"x=[-]?[0-9]+,{1} {1}y=[-]?[0-9]+", line)
        assert len(result) == 2
        sensor = parse_coords(result[0])
        beacon = parse_coords(result[1])
        print(sensor, beacon)
        sensorlist.append([sensor,beacon])



no_beacon = set()
beacons_in_row = set()
for item in sensorlist:
    sensor, beacon = item
    sx, sy = sensor
    bx, by = beacon
    # check if beacon in row
    if by == row:
        print("found beacon is row",sensor, beacon)
        beacons_in_row.add(beacon)

    manhattan_distance = abs(by - sy) + abs(bx - sx)    
    # if row is further than the nearest beacon 
    if abs(row - sy) > manhattan_distance:
        # sensor does not reach row, no info gained
        continue    
    # if sy does reach desired row, calculate remaining steps left
    steps = manhattan_distance - abs(row - sy)
    for x in range(sx-steps, sx+steps+1, 1):
        no_beacon.add((x, row))

temp = len(no_beacon)
for beacon in beacons_in_row:
    if beacon in no_beacon:
        temp -= 1

print("ANSWER part1", temp)

def compare(left, right):
    if left[0] == right[0]:
        return 0
    if left[0] < right[0]:
        return -1
    if left[0] > right[0]:
        return 1

print('part2')

no_beacon = set()
beacons_in_row = set()
rowtracker = [[] for _ in range(maxrow)]
print("GOT HERE")

for item in sensorlist:        
    sensor, beacon = item
    sx, sy = sensor
    bx, by = beacon        
    manhattan_distance = abs(by - sy) + abs(bx - sx)
    print("DIST:", sensor, manhattan_distance)    
    
    start = sy - manhattan_distance
    start = start if start >= 0 else 0
    end = sy + manhattan_distance + 1
    end = end if end <= maxrow else maxrow
    for row in range(start, end, 1):
        steps = manhattan_distance - abs(row - sy)        
        brange = (sx - steps, sx + steps)
        if brange[0] < 0:
            brange = (0, brange[1])
        if brange[1] < 1:
            brange = (brange[0], 0)
        if brange[0] > maxrow:
            brange = (maxrow, brange[1])
        if brange[1] > maxrow:
            brange = (brange[0], maxrow)
        # print("ROW", row)
        rowtracker[row].append(brange)        
    # for x in range(sx-steps, sx+steps+1, 1):
    #     rowtracker[row].discard(x)

#rowtracker = sorted(rowtracker, key=functools.cmp_to_key(compare))
#print(rowtracker)
for y, row in enumerate(rowtracker):
    row = sorted(row, key=functools.cmp_to_key(compare))
    # print(row)
    for i in range(len(row) - 1):
        if row[i][0] <= row[i + 1][0] <= row[i][1] + 1:
            # they overlap
            if row[i][1] > row[i + 1][1]:
                row[i+1] = row[i]
        else:
            # NO OVERLAP WE FOUND IT!
            x = row[i][1] + 1            
            answer = x * 4000000 + y
            print(row[i], row[i+1], "FOUND IT", x, y, answer)
            exit()


# print(rowtracker)
# for row, cols in rowtracker.items():
#     if len(cols) == 1:
#         col = list(cols)[0]
#         print("ANSWER", col * 4000000 + row)
