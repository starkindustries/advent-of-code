import math
import pprint


def print_tile(tile):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(tile)


ROTATIONS = [0, 90, 180, 270]
NONE, HORIZONTAL, VERTICAL, BOTH = 0, 1, 2, 3
FLIPS = [NONE, HORIZONTAL, VERTICAL, BOTH]


def rotate_tile(tile, angle):
    if angle == 0:
        return tile
    if angle == 90:
        new_tile = []
        for col in range(10):
            new_row = ''
            for row in range(9, -1, -1):
                new_row += tile[row][col]
            new_tile.append(new_row)
        return tuple(new_tile)
    if angle == 180:
        # reverse all rows and reverse order of rows
        return tuple(reversed([row[::-1] for row in tile]))
    if angle == 270:
        new_tile = []
        for col in range(9, -1, -1):
            new_row = ''
            for row in range(10):
                new_row += tile[row][col]
            new_tile.append(new_row)
        return tuple(new_tile)


def flip_tile(tile, flip):
    if flip == NONE:
        return tile
    if flip == HORIZONTAL:
        return tuple(row[::-1] for row in tile)
    if flip == VERTICAL:
        return tuple(reversed(tile))
    if flip == BOTH:
        return rotate_tile(tile, 180)


def orient(tile, angle, flip):
    assert flip in FLIPS and angle in ROTATIONS
    return rotate_tile(flip_tile(tile, flip), angle)


# ****************************
# Orientations (angle, flip)
# ****************************
# 1: [(0, 0), (180, 3)]
# 2: [(90, 0), (270, 3)]
# 3: [(180, 0), (0, 3)]
# 4: [(270, 0), (90, 3)]
# 5: [(0, 1), (180, 2)]
# 6: [(90, 1), (270, 2)]
# 7: [(180, 1), (0, 2)]
# 8: [(270, 1), (90, 2)]
def get_orientations():
    tile1427 = (
        '###.##.#..',
        '.#..#.##..',
        '.#.##.#..#',
        '#.#.#.##.#',
        '....#...##',
        '...##..##.',
        '...#.#####',
        '.#.####.#.',
        '..#..###.#',
        '..##.#..#.')
    tiles = {}
    for flip in FLIPS:
        for angle in ROTATIONS:
            new_tile = orient(tile1427, angle, flip)
            # new_tile = flip_tile(tile1427, flip)
            # new_tile = rotate_tile(new_tile, angle)
            tiles.setdefault(new_tile, [])
            tiles[new_tile].append((angle, flip))
    orientations = []
    for _, values in tiles.items():
        print(f"values: {values}")
        # Ignore orientations that produce the same tile:
        orientations.append(values[0])
    return tuple(orientations)


ORIENTATIONS = get_orientations()


def matches(t1, t2, tiles, horizontal):
    tile1 = orient(tiles[t1[0]], t1[1], t1[2])
    tile2 = orient(tiles[t2[0]], t2[1], t2[2])

    if horizontal:
        for row in range(len(tile1)):
            if tile1[row][9] != tile2[row][0]:
                return False
        return True
    # Vertical
    return tile1[9] == tile2[0]


def tile_valid(graph, tile, tiles, length):
    # the tile to be checked should not already be in the graph
    assert tile[0] not in [item[0] for item in graph]

    # if graph is empty, then any tile is valid
    if not graph:
        return True

    # check adjacent tiles for edges to match
    # 0 1 2
    # 3 4 5  above tiles: all positions > 2
    # 6 7 8  left tiles: all positions (index % 3) > 0
    pos = len(graph)
    # check above tile
    if pos >= length:
        top_tile = graph[pos - length]
        if not matches(top_tile, tile, tiles, False):
            return False
    # check left tile
    if (pos % length) > 0:
        left_tile = graph[pos - 1]
        if not matches(left_tile, tile, tiles, True):
            return False
    return True


def assemble(graph, tiles, length):
    if len(graph) == length ** 2:
        return graph

    for num in tiles.keys():
        if num in [item[0] for item in graph]:
            continue
        for angle, flip in ORIENTATIONS:
            tile = (num, angle, flip)
            if tile_valid(graph, tile, tiles, length):
                new_graph = graph[:]
                new_graph.append(tile)
                if assemble(new_graph, tiles, length):
                    return new_graph
    return False  # no valid graph found


def parse_input(filename):
    with open(filename, 'r') as handle:
        lines = handle.readlines()

    tiles = {}  # tiles[num] = [image rows]
    image = []
    tile_num = None
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        elif len(image) == 9:
            image.append(line)
            tiles[tile_num] = image[:]
            image = []
        elif "Tile" in line:
            tile_num = int(line.replace(':', '').split(" ")[1])
        else:
            image.append(line)

    pp = pprint.PrettyPrinter(indent=2)
    for key, image in tiles.items():
        print(key)
        pp.pprint(image)
    return tiles


def solve(filename):
    tiles = parse_input(filename)

    # get length of image
    length = int(math.sqrt(len(tiles)))
    graph = []
    graph = assemble(graph, tiles, length)

    # get the product of the four corners:
    print(f"GRAPH: {graph}")
    if not graph:
        return False
    result = graph[0][0] * graph[length-1][0] * \
        graph[length**2-1][0] * graph[length**2-length][0]
    print(f"RESULT: {result}")
    return result


# Test input parsing
tiles = parse_input("./20/sample.txt")
assert tiles[1427] == ['###.##.#..',
                       '.#..#.##..',
                       '.#.##.#..#',
                       '#.#.#.##.#',
                       '....#...##',
                       '...##..##.',
                       '...#.#####',
                       '.#.####.#.',
                       '..#..###.#',
                       '..##.#..#.']

# Test tile_valid function
# any tile is valid for empty graph
assert tile_valid([], (1427, 0, 0), tiles, 3)
tile_map = parse_input("./20/test1.txt")
# tile matches first tile in graph
assert tile_valid([(1951, 0, 0)], (2311, 0, 0), tiles, 3)

assert solve("./20/test2.txt") == 17558391313363
assert solve("./20/sample.txt") == 20899048083289
