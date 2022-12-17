import copy

# import sys
# sys.setrecursionlimit(1500)


def get_height(coord, heightmap):
    assert len(coord) == 2
    x, y = coord
    height = heightmap[y][x]
    if height == "S":
        return "a"
    if height == "E":
        return "z"
    return height


def height_diff(start, end, heightmap, part1):
    start_height = get_height(start, heightmap)
    end_height = get_height(end, heightmap)
    if part1:
        return ord(end_height) - ord(start_height)
    else:
        return ord(start_height) - ord(end_height)


def is_right_path_shorter(left, right):
    if not right:
        return False
    if not left:
        # no left path, keep the right one
        return True
    if len(left) < len(right):
        return False
    return True


# def search(path):
#     position = path[len(path) - 1]
#     if not path:
#         print("Error: found None for path:", position, path)
#         return None
#     if not position:
#         print("Error: found None for position:", position, path)
#         return None
#     if position == end_position:
#         return path

#     x, y = position
#     # search adjacent positions that are not already visited
#     next_positions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
#     old_path = None
#     for next in next_positions:
#         path_copy = path.copy()
#         if not (0 <= next[0] < num_cols and 0 <= next[1] < num_rows):
#             continue
#         if height_diff(position, next) > 1:
#             continue
#         if next in path_copy:
#             continue
#         path_copy.append(next)
#         if is_right_path_shorter(path_copy, old_path):
#             continue
#         new_path = search(path_copy)
#         if is_right_path_shorter(old_path, new_path):
#             old_path = new_path
#     if old_path:
#         return old_path
#     return None


def get_neighbors(position, heightmap):
    x, y = position
    num_rows = len(heightmap)
    num_cols = len(heightmap[0])
    possible_neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    neighbors = []
    for neighbor in possible_neighbors:
        if not (0 <= neighbor[0] < num_cols and 0 <= neighbor[1] < num_rows):
            continue
        if height_diff(position, neighbor, heightmap) > 1:
            continue
        neighbors.append(neighbor)
    return neighbors


def bfs_search(start, heightmap, part1=True):
    edge_len = 1
    queue = [start]
    distances = []
    num_rows = len(heightmap)
    num_cols = len(heightmap[0])

    for _ in range(len(heightmap)):
        distances.append([-1 for x in range(len(heightmap[0]))])
    start_x, start_y = start
    distances[start_y][start_x] = 0

    while queue:
        node = queue.pop(0)
        node_x, node_y = node
        neighbors = [
            (node_x - 1, node_y),
            (node_x + 1, node_y),
            (node_x, node_y - 1),
            (node_x, node_y + 1),
        ]
        for neighbor in neighbors:
            if not (0 <= neighbor[0] < num_cols and 0 <= neighbor[1] < num_rows):
                continue
            if height_diff(node, neighbor, heightmap, part1) > 1:
                continue
            x, y = neighbor
            if distances[y][x] == -1:
                distances[y][x] = distances[node_y][node_x] + edge_len
                queue.append(neighbor)
        # do stuff
    return distances


def solve(filename):
    END = "E"
    START = "S"
    end_position = ()
    heightmap = []
    start_position = (0, 0)
    a_positions = set()

    with open(filename, "r", encoding="utf8") as handle:
        for y, line in enumerate(handle):
            line = line.strip()
            row = []
            for x, tile in enumerate(line):
                if tile == END:
                    end_position = (x, y)
                elif tile == START:
                    start_position = (x, y)
                    a_positions.add((x, y))
                elif tile == "a":
                    a_positions.add((x, y))
                row.append(tile)
            heightmap.append(row)

    # result = []
    distances = bfs_search(start_position, heightmap)
    print(distances)
    x, y = end_position
    print("end", end_position)
    print("DISTANCE", distances[y][x])
    part1 = distances[y][x]
    # if result == None:
    #     print("ERROR: result set to None:", result)
    # if end_position not in result:
    #     print("Error: end position not found in path:", result)

    # print(result)
    # length = len(result)
    # print(length)
    # print("STEPS", length - 1)

    # mapcopy = copy.deepcopy(heightmap)
    # for i, pos in enumerate(result):
    #     x, y = pos
    #     mapcopy[y][x] = i

    # for row in mapcopy:
    #     row_output = ""
    #     for element in row:
    #         element = str(element)
    #         spaces = 3 - len(element)
    #         row_output += " " * spaces + element
    #     print(row_output)

    # return length - 1

    # Part 2

    # distances2 = bfs_search(end_position, heightmap)
    min_distance = float("inf")
    for a_pos in a_positions:
        distances = bfs_search(a_pos, heightmap)
        endx, endy = end_position
        if distances[endy][endx] < 0:
            continue
        if distances[endy][endx] < min_distance:
            min_distance = distances[endy][endx]
    print("Part 2:", min_distance)
    part2 = min_distance
    return part1, part2


part1, part2 = solve("sample.txt")
assert part1 == 31
assert part2 == 29

# print()
solve("input.txt")
# not 418
