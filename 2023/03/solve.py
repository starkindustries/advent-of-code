
with open("input.txt") as file:
    lines = file.readlines()

# part 1
def is_symbol(char):
    if char.isdigit() or char == ".":
        return False
    return True

def is_part_number(map, x, y):
    deltas = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    for d in deltas:
        dx = x + d[0]
        dy = y + d[1]
        if dx < 0 or dx >= len(map[0]):
            continue
        if dy < 0 or dy >= len(map):
            continue
        if is_symbol(map[dy][dx]):
            return True
    return False

def is_adjacent(x, y, locations):
    deltas = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    for d in deltas:
        dx = x + d[0]
        dy = y + d[1]
        if (dx, dy) in locations:
            return True
    return False

total = 0

mymap = []
for line in lines:
    mymap.append(line.strip())

print(mymap)

# get all part numbers
parts = []
gears = []
for y in range(len(mymap)):
    locations = []
    part_number = ""
    print(mymap[y])
    for x in range(len(mymap[0])):
        char = mymap[y][x]
        if char.isdigit():
            part_number += char
            locations.append((x, y))
        elif len(part_number) > 0:
            # add to parts
            parts.append((part_number, locations))
            part_number = ""
            locations = []
        # FOR PART 2
        if char == "*":
            gears.append((x, y))
    # add to parts
    if len(part_number) > 0:
        parts.append((part_number, locations))
        part_number = ""
        locations = []

# for part in parts:
#     print(part, parts[part])

print(parts)

# loop through all part locations
for part_tuple in parts:
    part_num, locations = part_tuple
    for location in locations:
        if is_part_number(mymap, location[0], location[1]):
            total += int(part_num)
            break

print(total)

# part 2

print("gears", gears)
total = 0
for gear in gears:
    x, y = gear
    parts_adjacent = []
    # count adjacent parts
    for part_tuple in parts:
        part_num, locations = part_tuple
        if is_adjacent(x, y, locations):
            parts_adjacent.append(part_num)
        if len(parts_adjacent) > 2:
            break
    print(gear, "parts adj", parts_adjacent)
    if len(parts_adjacent) == 2:
        print("ADJ PARTS:", parts_adjacent)
        total += int(parts_adjacent[0]) * int(parts_adjacent[1])
print(total)