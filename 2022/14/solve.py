def solve():
    pass


lines = []

filename = "input.txt"
with open(filename, "r", encoding="utf8") as handle:
    for line in handle:
        line = line.strip().split("->")
        points = [tuple(map(int, x.split(","))) for x in line]
        lines.append(points)

rocks = set()  # (x, y)

# build rocks
for line in lines:
    # iterate through each point
    for i in range(len(line) - 1):
        x1, y1 = line[i]
        x2, y2 = line[i + 1]
        if x1 == x2:
            sign = 1 if y2 > y1 else -1
            for dy in range(y1, y2 + sign, sign):
                rocks.add((x1, dy))
        elif y1 == y2:
            sign = 1 if x2 > x1 else -1
            for dx in range(x1, x2 + sign, sign):
                rocks.add((dx, y1))

print(rocks)
# find rock with lowest y value
lowest_rock = None
for rock in rocks:
    if lowest_rock is None:
        lowest_rock = rock
    if rock[1] > lowest_rock[1]:
        lowest_rock = rock


def is_sand_resting(position, rocks, sand, lowest_y):
    assert position not in rocks

    while True:
        x, y = position
        if y > lowest_y:
            # infinity drop
            return False
        down, downleft, downright = (x, y + 1), (x - 1, y + 1), (x + 1, y + 1)
        # check down, down-left, down-right
        if down not in rocks and down not in sand:
            position = down
        elif downleft not in rocks and downleft not in sand:
            position = downleft
        elif downright not in rocks and downright not in sand:
            position = downright
        else:
            sand.add(position)
            return True


def part2(position, rocks, sand, lowest_y):
    assert position not in rocks
    if position in sand:
        return False
    while True:
        # print(position, lowest_y)
        x, y = position
        if y >= lowest_y - 1:
            # print(position)
            sand.add(position)
            return True
        down, downleft, downright = (x, y + 1), (x - 1, y + 1), (x + 1, y + 1)
        # check down, down-left, down-right
        if down not in rocks and down not in sand:
            position = down
        elif downleft not in rocks and downleft not in sand:
            position = downleft
        elif downright not in rocks and downright not in sand:
            position = downright
        else:
            # print(position)
            sand.add(position)
            return True


sand_start = (500, 0)
sand = set()
count = 0

while is_sand_resting(sand_start, rocks, sand, lowest_rock[1]):
    count += 1

print("count", count)

count = 0
sand = set()
while part2(sand_start, rocks, sand, lowest_rock[1] + 2):
    count += 1

print("PART2", count)
