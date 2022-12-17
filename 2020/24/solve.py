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
        if line[i] in ["n", "s"]:
            y += -1 if line[i] == "s" else 1
            i += 1
            is_cardinal = False
        if line[i] in ["e", "w"]:
            offset = 1 + is_cardinal
            x += -offset if line[i] == "w" else offset
        i += 1
    return x, y


def get_adj_tiles(x, y, black_tiles):
    # East
    black, white = set(), set()
    if (x + 2, y) in black_tiles:
        black.add((x + 2, y))
    else:
        white.add((x + 2, y))
    # West
    if (x - 2, y) in black_tiles:
        black.add((x - 2, y))
    else:
        white.add((x - 2, y))
    # NorthEast
    if (x + 1, y + 1) in black_tiles:
        black.add((x + 1, y + 1))
    else:
        white.add((x + 1, y + 1))
    # NorthWest
    if (x - 1, y + 1) in black_tiles:
        black.add((x - 1, y + 1))
    else:
        white.add((x - 1, y + 1))
    # SouthEast
    if (x + 1, y - 1) in black_tiles:
        black.add((x + 1, y - 1))
    else:
        white.add((x + 1, y - 1))
    # SouthWest
    if (x - 1, y - 1) in black_tiles:
        black.add((x - 1, y - 1))
    else:
        white.add((x - 1, y - 1))
    return black, white


def flip(black_tiles):
    new_black_tiles = set()
    white_tiles = set()
    for x, y in black_tiles:
        black_adj, white_adj = get_adj_tiles(x, y, black_tiles)
        white_tiles.update(white_adj)
        # Any black tile with zero or more than 2 black tiles
        # immediately adjacent to it is flipped to white.
        if len(black_adj) == 0 or len(black_adj) > 2:
            # tile gets flipped to white
            continue
        else:  # tile remains black
            new_black_tiles.add((x, y))

    # Any white tile with exactly 2 black tiles immediately
    # adjacent to it is flipped to black.
    for x, y in white_tiles:
        black_adj, _ = get_adj_tiles(x, y, black_tiles)
        if len(black_adj) == 2:
            new_black_tiles.add((x, y))
    return new_black_tiles


def solve(filename, days=None):
    with open(filename) as handle:
        lines = [line.strip() for line in handle]

    # Part 1 and Part 2
    black_tiles = set()
    for line in lines:
        x, y = parse_directions(line)
        if (x, y) in black_tiles:
            black_tiles.remove((x, y))
        else:
            black_tiles.add((x, y))

    # Part 1
    if days is None:
        result = len(black_tiles)
        print(f"Part 1: {result}")
        return result

    # Part 2
    for _ in range(days):
        black_tiles = flip(black_tiles)
    result = len(black_tiles)
    print(f"Part 2: {result}")
    return result


# Part 1
assert solve("sample.txt") == 10
assert solve("input.txt") == 293

# Part 2
assert solve("sample.txt", 1) == 15
assert solve("sample.txt", 2) == 12
assert solve("sample.txt", 3) == 25
assert solve("sample.txt", 4) == 14
assert solve("sample.txt", 5) == 23
assert solve("sample.txt", 6) == 28
assert solve("sample.txt", 7) == 41
assert solve("sample.txt", 8) == 37
assert solve("sample.txt", 9) == 49
assert solve("sample.txt", 10) == 37
assert solve("sample.txt", 20) == 132
assert solve("sample.txt", 30) == 259
assert solve("sample.txt", 40) == 406
assert solve("sample.txt", 50) == 566
assert solve("sample.txt", 60) == 788
assert solve("sample.txt", 70) == 1106
assert solve("sample.txt", 80) == 1373
assert solve("sample.txt", 90) == 1844
assert solve("sample.txt", 100) == 2208
assert solve("input.txt", 100) == 3967
