import math



# imageLen = Count the number of tiles and get the sq root
# for i in range(tileCount):
#   for o in orientations:
#     place a new tile (graph, tiles, position)
#     if no valid tiles exist
#       return False
# print graph
# return graph

# first tile can be any orientation or any tile


#
# blank graph. place a tile (any tile, any orientation)
# update graph
# remove tile from tiles list.
# recurse.


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
# 5) 4 3 2 1 => c2 b2 a2 d2
# 6) 3 2 1 4 => b2 a2 d2 c2
# 7) 2 1 4 3 => top2 left2 bottom2 right2
def get_edge(tile, orientation, side):
    if orientation == 0:
        return tile
    elif orientation == 1:
        return 
    elif orientation == 2:
        pass
    elif orientation == 3:
        pass
    elif orientation == 4:
        pass
    elif orientation == 5:
        pass
    elif orientation == 6:
        pass
    elif orientation == 7:
        pass
# def placeTile(graph, tiles, position):
#   check adjacent tiles for this position
#   
#   if no valid tiles exist:
#      return False
#   return graph



    
# graph is an array of tuples: (tile, orientation)
# tile is an array of edges (strings)
# orientation is a number from 1 to 8, as noted in "Orientations" section

# def solve(tile, )
#   if not tiles:
#      return graph
#   if no valid tiles:
#      return False
#   place tile
def assemble(tiles, graph=[], tiles_dict, edges, side_len):
    if not graph:
        for num, _ in tiles_dict.items():
            for o in orientations:
                tiles.remove(num)
                result = assemble(tiles, [(num, o)], tiles_dict, edges)
                if result:
                    return result
        raise RuntimeError("Error: No solution found.")
    if not tiles:
        return graph
    
    # place tile
    pos = len(graph)

    # check adjacent tiles for edges to match
    # 0 1 2
    # 3 4 5  above tiles: all positions > 2
    # 6 7 8  left tiles: all positions (index % 3) > 0

    # check left tile
    if (pos % side_len) > 0:
        tile_left, orientation = graph[pos - 1]
        edge = get_edge(tiles[tile_left], orientation)
        matching_tiles = set(edges[edge])
    # check above tile
    if open_index > (side_len - 1):
        tile_above, orientation = graph[open_index-image_len]
        edge = get_edge(tiles[tile_above], orientation)
        matching_tiles = matching_tiles & set(edges[edge])
    # loop through matching tiles
    for tile in matching_tiles:
        new_tiles = tiles[:].remove(tile)
        result = assemble(new_tiles, graph[:].append((tile, orientation)), tiles_dict, edges)
        if result:
            return result
    # no matching tiles
    return False


def print_tile(edges, separator=" "):
    # print top
    for col in range(10):
        print(edges[0][col], end=separator)
    print()
    # print left and right
    for row in range(1, 9):
        # left edge
        print(edges[5][row], end=separator+("_"+separator)*8)
        # right edge
        print(edges[1][row])
    # print bottom edge
    for col in range(10):
        print(edges[6][col], end=separator)
    print()


def get_edges(number, image, edges):
    top = image[0]
    # bottom should go from right to left
    bottom = image[9][::-1]
    left, right = "", ""
    for row in range(10):
        left += image[row][0]
        right += image[row][9]
    # left should go from bottom to top
    left = left[::-1]
    print(f"left: {left}")
    print(f"right: {right}")
    for i, e in enumerate([top, right, bottom, left]):
        edges.setdefault(e, [])
        if (number, i) not in edges[e]:
            edges[e].append((number, i))


# solve
def solve(filename):
    # Process input
    tiles = {}
    edges = {}
    tile_count = 0
    with open(filename, 'r') as handle:
        tile_num = None
        image = []
        for line in handle:
            line = line.strip()
            if line == "":
                continue
            elif len(image) == 9:
                print(f"LINE: {line}")
                print(f"Tile {tile_num}:")
                image.append(line)
                tiles[tile_num] = image[:]
                get_edges(tile_num, image, edges)
                print_tile(tiles[tile_num])
                tile_num, image = None, []
                tile_count += 1
            elif tile_num is None:
                tile_num = int(line.replace(":", "").split(" ")[1])
            else:
                image.append(line)
    image_len = math.sqrt(tile_count)
    print(f"IMAGE LEN: {image_len}")
    # tile = next(iter(tiles))
    # graph = assemble(tiles)
    print("EDGES")
    print(edges)


assert solve("sample.txt") == 20899048083289
