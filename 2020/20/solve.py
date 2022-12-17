import math
import functools


ROTATIONS = [0, 90, 180, 270]
NONE, HORIZONTAL, VERTICAL, BOTH = 0, 1, 2, 3
FLIPS = [NONE, HORIZONTAL, VERTICAL, BOTH]


def rotate_tile(tile, angle):
    length = len(tile[0])
    if angle == 0:
        return tile
    if angle == 90:
        new_tile = []
        for col in range(length):
            new_row = ""
            for row in range(length - 1, -1, -1):
                new_row += tile[row][col]
            new_tile.append(new_row)
        return tuple(new_tile)
    if angle == 180:
        # reverse all rows and reverse order of rows
        return tuple(reversed([row[::-1] for row in tile]))
    if angle == 270:
        new_tile = []
        for col in range(length - 1, -1, -1):
            new_row = ""
            for row in range(length):
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


@functools.lru_cache(maxsize=None)
def orient(tile, angle, flip):
    # assert flip in FLIPS and angle in ROTATIONS
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
        "###.##.#..",
        ".#..#.##..",
        ".#.##.#..#",
        "#.#.#.##.#",
        "....#...##",
        "...##..##.",
        "...#.#####",
        ".#.####.#.",
        "..#..###.#",
        "..##.#..#.",
    )
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
    # assert tile[0] not in [item[0] for item in graph]

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


def assemble(tiles, length, graph=[]):
    if len(graph) == length**2:
        return graph

    for num in tiles.keys():
        if num in [item[0] for item in graph]:
            continue
        for angle, flip in ORIENTATIONS:
            tile = (num, angle, flip)
            if tile_valid(graph, tile, tiles, length):
                new_graph = graph[:]
                new_graph.append(tile)
                if new_graph := assemble(tiles, length, new_graph):
                    return new_graph
    return False  # no valid graph found


def parse_input(filename):
    with open(filename, "r") as handle:
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
            tiles[tile_num] = tuple(image)
            image = []
        elif "Tile" in line:
            tile_num = int(line.replace(":", "").split(" ")[1])
        else:
            image.append(line)
    return tiles


def stitch(graph, tiles, length):
    stitched_image = [""] * 8 * length
    offset = 0
    for i, tile in enumerate(graph):
        num, angle, flip = tile
        image = orient(tiles[num], angle, flip)
        # remove borders from image
        image = image[1:9]
        image = [row[1:9] for row in image]
        if i > 0 and i % length == 0:
            # move on to next image row
            offset += 1
        for j in range(len(image)):
            stitched_image[j + offset * 8] += image[j]

    return tuple(stitched_image)


def search_sea_dragons(image):
    #          00000000001111111111 x-axis
    #          01234567890123456789
    dragon = [
        "                  # ",  # 0
        "#    ##    ##    ###",  # 1 y-axis
        " #  #  #  #  #  #   ",
    ]  # 2
    dragon_height = len(dragon)  # 3
    dragon_length = len(dragon[0])  # 20

    # Gather the offsets of the dragon's body
    dragon_offsets = []
    for y in range(dragon_height):
        for x in range(dragon_length):
            if dragon[y][x] == "#":
                dragon_offsets.append((x, y))

    locations = []
    for row in range(len(image) - dragon_height + 1):
        for col in range(len(image) - dragon_length + 1):
            is_dragon = True
            for x, y in dragon_offsets:
                if image[row + y][col + x] != "#":
                    is_dragon = False
                    break
            if is_dragon:
                locations.append((col, row))  # (x, y) location
    return locations


def solve(filename, part2=False):
    # *************
    # Part 1
    # *************
    tiles = parse_input(filename)

    # get length of image
    length = int(math.sqrt(len(tiles)))
    graph = assemble(tiles, length)

    if not graph:
        return False

    if not part2:
        # get the product of the four corners:
        part1 = (
            graph[0][0]
            * graph[length - 1][0]
            * graph[length**2 - 1][0]
            * graph[length**2 - length][0]
        )
        print(f"Part 1: {part1}")
        return part1

    # *************
    # Part 2
    # *************
    stitched = stitch(graph, tiles, length)
    for angle, flip in ORIENTATIONS:
        orient(stitched, angle, flip)
        if len(locations := search_sea_dragons(stitched)) > 0:
            break
    # By manually inspecting the dragon locations, none overlap.
    # Therefore, ignore edge case of overlapping dragons.
    # Count the number of '#' and then subtract the number of
    # dragons multiplied by number of dragon parts (15)
    part2 = sum([row.count("#") for row in stitched]) - len(locations) * 15
    print(f"Part 2: {part2}")
    return part2


def test_input_parsing():
    tiles = parse_input("sample.txt")
    assert tiles[1427] == (
        "###.##.#..",
        ".#..#.##..",
        ".#.##.#..#",
        "#.#.#.##.#",
        "....#...##",
        "...##..##.",
        "...#.#####",
        ".#.####.#.",
        "..#..###.#",
        "..##.#..#.",
    )


def test_tile_valid():
    tiles = parse_input("sample.txt")

    # any tile is valid for empty graph
    assert tile_valid([], (1427, 0, 0), tiles, 3)

    # tile matches first tile in graph
    assert tile_valid([(1951, 0, 0)], (2311, 0, 0), tiles, 3)


def test_stitch():
    tiles = parse_input("sample.txt")
    length = int(math.sqrt(len(tiles)))
    graph = assemble(tiles, length)
    with open("test3.txt") as handle:
        lines = [line.strip() for line in handle]
    stitched = orient(stitch(graph, tiles, length), 90, VERTICAL)
    assert stitched == tuple(lines)


def test_search_sea_dragon():
    with open("test4.txt") as handle:
        lines = tuple([line.strip() for line in handle])
    locations = search_sea_dragons(lines)
    assert len(locations) == 2
    assert (2, 2) in locations
    assert (1, 16) in locations


# Run tests
test_tile_valid()
test_stitch()
test_search_sea_dragon()

# Part 1
assert solve("test2.txt") == 17558391313363
assert solve("sample.txt") == 20899048083289
assert solve("input.txt") == 7492183537913

# Part 2
assert solve("sample.txt", True) == 273
assert solve("input.txt", True) == 2323
