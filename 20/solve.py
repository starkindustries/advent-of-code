import math
import pprint

# *******************
# Constants
# *******************
TOP, RIGHT, BOTTOM, LEFT = 0, 1, 2, 3
num_orientations = 8

# *******************
# Orientations
# *******************
# Terms:
# corners = 1, 2, 3, 4
# normal edges   top = 1 2,   right = 2 3,   bottom = 3 4,   left = 4 1
# flipped edges top2 = 2 1, right2 = 3 2, bottom2 = 4 3, left2 = 1 4

# normal:
# 0) 1 2 3 4 => top right bottom left
# 1) 2 3 4 1 => right bottom left top
# 2) 3 4 1 2 => bottom left top right
# 3) 4 1 2 3 => left top right bottom
# flipped:
# 4) 1 4 3 2 => left2 bottom2 right2 top2
# 5) 4 3 2 1 => bottom2 right2 top2 left2
# 6) 3 2 1 4 => right2 top2 left2 bottom2
# 7) 2 1 4 3 => top2 left2 bottom2 right2


class Tile:
    def __init__(self, image, o=None):
        self.orientation = o
        self.image = image[:]
        self.top = image[0]
        self.bottom = image[9]
        self.left, self.right = "", ""
        for row in image:
            self.left += row[0]
            self.right += row[9]

    def get_side(self, side):
        if self.orientation == 0:
            return [self.top, self.right, self.bottom, self.left][side]
        elif self.orientation == 1:
            return [self.right, self.bottom, self.left, self.top][side]
        elif self.orientation == 2:
            return [self.bottom, self.left, self.top, self.right][side]
        elif self.orientation == 3:
            return [self.left, self.top, self.right, self.bottom][side]
        elif self.orientation == 4:
            return [self.left[::-1], self.bottom[::-1], self.right[::-1], self.top[::-1]][side]
        elif self.orientation == 5:
            return [self.bottom[::-1], self.right[::-1], self.top[::-1], self.left[::-1]][side]
        elif self.orientation == 6:
            return [self.right[::-1], self.top[::-1], self.left[::-1], self.bottom[::-1]][side]
        elif self.orientation == 7:
            return [self.top[::-1], self.left[::-1], self.bottom[::-1], self.right[::-1]][side]

    def matches(self, side1, tile2, side2):
        return self.get_side(side1) == tile2.get_side(side2)


def tile_valid(graph, tile_num, orientation, tiles, side_len):
    # if graph is empty, then any tile is valid
    if not graph:
        return True

    # check adjacent tiles for edges to match
    # 0 1 2
    # 3 4 5  above tiles: all positions > 2
    # 6 7 8  left tiles: all positions (index % 3) > 0
    tile = Tile(tiles[tile_num].image, orientation)
    pos = len(graph)
    if pos >= side_len:  # check above tile
        t, o = graph[pos - side_len]
        above_tile = Tile(tiles[t].image, o)
        if not above_tile.matches(BOTTOM, tile, TOP):
            return False
    if (pos % side_len) > 0:  # check left tile
        t, o = graph[pos - 1]
        left_tile = Tile(tiles[t].image, o)
        if not left_tile.matches(RIGHT, tile, LEFT):
            return False
    return True


# graph: list of tuples: [(tile #, orientation), (t, o), ...]
# tiles: list of tile numbers, e.g. [1951, 2311, 3079]
# side_len: the length of the side of the full image

def assemble(graph, tiles, side_len):
    if len(tiles) > 0:
        for t in tiles:
            for o in range(num_orientations):
                if tile_valid(graph, t, o, tiles, side_len):
                    graph.append((t, o))
                    tiles.remove(t)
                    if assemble(graph, tiles, side_len):
                        return graph
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
            tiles[tile_num] = Tile(image)
            image = []
        elif "Tile" in line:
            tile_num = int(line.replace(':', '').split(" ")[1])
        else:
            image.append(line)

    pp = pprint.PrettyPrinter(indent=2)
    for key, value in tiles.items():
        print(key)
        pp.pprint(value.image)
    return tiles


tiles = parse_input("./20/sample.txt")
assert tiles[1427].image == ['###.##.#..', '.#..#.##..', '.#.##.#..#', '#.#.#.##.#',
                             '....#...##', '...##..##.', '...#.#####', '.#.####.#.', '..#..###.#', '..##.#..#.']

assert tile_valid([], 10, 0, tiles, 3)

tiles = parse_input("./20/test1.txt")
assert tile_valid([(1951, 0)], 2311, 0, tiles, 3)

# assert solve("sample.txt") == 20899048083289
