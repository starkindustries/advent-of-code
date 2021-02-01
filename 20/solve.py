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
            new_tile = flip_tile(tile1427, flip)
            new_tile = rotate_tile(new_tile, angle)
            tiles.setdefault(new_tile, [])
            tiles[new_tile].append((angle, flip))
    orientations = []
    for _, values in tiles.items():
        print(f"values: {values}")
        orientations.append(values[0])
    return tuple(orientations)

get_orientations()
exit()

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

# 1 2    2 1
# 3 4 => 4 3 flip horizontal

# normal edges   top = 1 2,  right = 2 3,  bottom = 3 4,  left = 4 1
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

    def get_edges(self):
        if self.orientation == 0:
            return [self.top, self.right, self.bottom, self.left]
        elif self.orientation == 1:
            return [self.right, self.bottom[::-1], self.left, self.top[::-1]]
        elif self.orientation == 2:
            return [self.bottom[::-1], self.left, self.top, self.right]
        elif self.orientation == 3:
            return [self.left, self.top, self.right, self.bottom]
        elif self.orientation == 4:
            return [self.left[::-1], self.bottom[::-1], self.right[::-1], self.top[::-1]]
        elif self.orientation == 5:
            return [self.bottom[::-1], self.right[::-1], self.top[::-1], self.left[::-1]]
        elif self.orientation == 6:
            return [self.right[::-1], self.top[::-1], self.left[::-1], self.bottom[::-1]]
        elif self.orientation == 7:
            return [self.top[::-1], self.left[::-1], self.bottom[::-1], self.right[::-1]]

    def get_side(self, side):
        return self.get_edges()[side]

    def matches(self, side1, tile2, side2):
        return self.get_side(side1) == tile2.get_side(side2)


def tile_valid(graph, tile_num, orientation, tile_map, side_len):
    # the tile to be checked should not already be in the graph
    if tile_num in [tup[0] for tup in graph]:
        return False

    # if graph is empty, then any tile is valid
    if not graph:
        return True

    # check adjacent tiles for edges to match
    # 0 1 2
    # 3 4 5  above tiles: all positions > 2
    # 6 7 8  left tiles: all positions (index % 3) > 0
    tile = Tile(tile_map[tile_num].image, orientation)
    pos = len(graph)
    if pos >= side_len:  # check above tile
        t, o = graph[pos - side_len]
        above_tile = Tile(tile_map[t].image, o)
        if not above_tile.matches(BOTTOM, tile, TOP):
            return False
    if (pos % side_len) > 0:  # check left tile
        t, o = graph[pos - 1]
        left_tile = Tile(tile_map[t].image, o)
        if not left_tile.matches(RIGHT, tile, LEFT):
            return False
    return True


def print_graph(graph, tile_map):
    for t, o in graph:
        print(f"t:{t}, o:{o}")
        tile = Tile(tile_map[t].image, o)
        edges = tile.get_edges()
        print(edges[0])
        for i in range(1, 9):
            print(f"{edges[3][i]}________{edges[1][i]}")
        print(edges[2])


# graph: list of tuples: [(tile #, orientation), (t, o), ...]
# tiles: list of tile numbers, e.g. [1951, 2311, 3079]
# side_len: the length of the side of the full image
def assemble(graph, tiles, tile_map, side_len):
    print(f"ASSEMBLE: tiles:{tiles}, graph:{graph}")
    print_graph(graph, tile_map)
    if len(graph) == side_len ** 2:
        return graph

    for tile in tiles:
        for o in range(num_orientations):
            if tile_valid(graph, tile, o, tile_map, side_len):
                temp_graph = graph[:]
                temp_graph.append((tile, o))
                temp_tiles = tiles[:]
                temp_tiles.remove(tile)
                if (temp_graph := assemble(temp_graph, temp_tiles, tile_map, side_len)):
                    return temp_graph
    return False  # no valid graph found

    # for t in tiles:
    #     tiles.remove(t)
    #     for o in range(num_orientations):
    #         print(f"IF_TILE_VALID: t:{t}, tiles:{tiles}, graph:{graph}")
    #         if tile_valid(graph, t, o, tile_map, side_len):
    #             graph.append((t, o))
    #             print(f"TILE_VALID: t:{t}, tiles:{tiles}, graph:{graph}")
    #             if assemble(graph[:], tiles[:], tile_map, side_len):
    #                 return graph
    #             else:
    #                 graph.remove((t, o))
    #     tiles.append(t)
    # return False  # no valid graph found


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


def solve(filename):
    tile_map = parse_input(filename)
    tiles = list(tile_map.keys())
    graph = []
    side_len = int(math.sqrt(len(tiles)))
    graph = assemble(graph, tiles, tile_map, side_len)
    # get the product of the four corners:
    print(f"GRAPH: {graph}")
    if not graph:
        return False
    result = graph[0][0] * graph[side_len-1][0] * \
        graph[side_len**2-1][0] * graph[side_len**2-side_len][0]
    print(f"RESULT: {result}")
    return result


"""
# Test input parsing
tile_map = parse_input("./20/sample.txt")
assert tile_map[1427].image == ['###.##.#..', '.#..#.##..', '.#.##.#..#', '#.#.#.##.#',
                                '....#...##', '...##..##.', '...#.#####', '.#.####.#.', '..#..###.#', '..##.#..#.']

# Test tile_valid function
# Case where any tile is valid for empty graph
assert tile_valid([], 10, 0, tile_map, 3)
# Case where tile matches up against first tile in graph
tile_map = parse_input("./20/test1.txt")
assert tile_valid([(1951, 0)], 2311, 0, tile_map, 3)
"""

# tile_map = parse_input("./20/sample.txt")
# result = assemble(graph, list(tile_map.keys()), tile_map, math.sqrt(len(tile_map)))
assert solve("./20/test2.txt") == 17558391313363
assert solve("./20/sample.txt") == 20899048083289
