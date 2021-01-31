# *****************
# Directions
# *****************
# nw .''. ne
# w |    | e
# sw '..' se

# ***********************************************
# Visualization of hexagons 'o' on a 2D plane
# ***********************************************
# y-axis
# 5
# 4     o   o
# 3   o   o   o   The center tile in this example is at (4, 3)
# 2     o   o
# 1
# 0 1 2 3 4 5 6  x-axis

# *****************************************************
# Changes in x,y when moving in a particular direction
# *****************************************************
# e : x+2
# se: x+1, y-1
# sw: x-1, y-1
# w : x-2
# nw: x-1, y+1
# ne: x+1, y+1

def parse_directions(line):
    x, y, i = 0, 0, 0
    while i < len(line):
        is_cardinal = True
        if line[i] in ['n', 's']:
            y += -1 if line[i] == 's' else 1
            i += 1
            is_cardinal = False
        if line[i] in ['e', 'w']:
            offset = 1 + is_cardinal
            x += -offset if line[i] == 'w' else offset
        i += 1
    return x, y


def flip(black_tiles):
    pass


# Track black tiles in a map
def solve(filename, days=0):
    with open(filename) as handle:
        lines = [line.strip() for line in handle]

    # Part 1
    black_tiles = set()
    for line in lines:
        x, y = parse_directions(line)
        if (x, y) in black_tiles:
            black_tiles.remove((x, y))
        else:
            black_tiles.add((x, y))

    part1 = len(black_tiles)
    print(f"Part 1: {part1}")

    # Part 2
    for _ in range(days):
        flip(black_tiles)

    return part1


assert solve("sample.txt") == 10
assert solve("input.txt") == 293
