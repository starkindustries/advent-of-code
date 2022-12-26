import sys
from copy import deepcopy


sys.setrecursionlimit(100000)

WALL = "#"
GROUND = "."
LEFT = "<"
RIGHT = ">"
UP = "^"
DOWN = "v"
BLIZZARD = (LEFT, RIGHT, UP, DOWN)
WIDTH = None
HEIGHT = None
ELF = "E"

open('map_printout.txt', 'w').close()


def print_map(width, height, walls, blizzards, elf, to_file=False):    
    if to_file:
        handle = open("map_printout.txt", "a", encoding="utf-8")
    for y in range(height):
        row = ""
        for x in range(width):
            if (x, y) == elf:
                # assert elf not in blizzards
                # assert elf not in walls
                row += ELF
            elif (x, y) in walls:
                row += WALL            
            elif (x, y) in blizzards:
                directions = blizzards[(x, y)]
                if len(directions) > 1:
                    row += str(len(directions))
                elif len(directions) == 1:
                    row += list(directions)[0]
            else:
                row += GROUND
        
        if to_file:
            handle.write(row + "\n")
        else:
            print(row)
    if to_file:
        handle.write("\n")

def check_blizzard_respawn(position, walls, direction):
    if position not in walls:
        return position
    if direction == LEFT:
        return (WIDTH - 2, position[1])
    elif direction == RIGHT:
        return (1, position[1])
    elif direction == UP:
        return (position[0], HEIGHT - 2)
    elif direction == DOWN:
        return (position[0], 1)
    assert False


OFFSETS = {
    RIGHT: ( 1,  0),
    LEFT:  (-1,  0),
    UP:    ( 0, -1),
    DOWN:  ( 0,  1),
}

def move_blizzards(blizzards, walls):
    new_blizzards = {}
    for position, directions in blizzards.items():
        for direction in directions:
            offset = OFFSETS[direction]
            new_position = (position[0] + offset[0], position[1] + offset[1])
            new_position = check_blizzard_respawn(new_position, walls, direction)
            new_blizzards.setdefault(new_position, set())
            new_blizzards[new_position].add(direction)
    return new_blizzards


def bfs_search(start, stop, blizzards, walls, width, height):
    edge_len = 1
    queue = [(start, blizzards, 0)]
    distances = []

    for _ in range(height):
        distances.append([-1 for _ in range(width)])
    start_x, start_y = start
    distances[start_y][start_x] = 0
    # min_steps = float("inf")

    while queue:
        elf, blizzards, steps = queue.pop(0)
        if elf == stop:
            return distances
                                
        # search for new position
        elf_x, elf_y = elf
        neighbors = [
            (elf_x - 1, elf_y),
            (elf_x + 1, elf_y),
            (elf_x, elf_y - 1),
            (elf_x, elf_y + 1),
        ]

        new_blizzards = move_blizzards(blizzards, walls)
        print_map(width, height, walls, new_blizzards, elf)
        steps += 1
        for neighbor in neighbors:
            if neighbor in walls or neighbor in new_blizzards \
                    or neighbor[1] <= 0 or neighbor[1] >= HEIGHT:
                # neighbor[1] == 0 is y at the starting point, do not consider
                continue
            x, y = neighbor
            # print((x, y))
            if distances[y][x] == -1:
                distances[y][x] = steps
            queue.append((neighbor, new_blizzards, steps))
        # check if waiting will put elf in a blizzard
        if elf not in new_blizzards and steps > 1:
            queue.append((elf, new_blizzards, steps))
    return distances


def distance_between(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x2 - x1) + abs(y2 - y1)

# MAX_VISITS = 5
# visited = {}
# min_steps = float("inf")
# def dfs_search(elf, stop, blizzards, walls, width, height, steps):
#     global min_steps    
#     if steps >= min_steps:
#         print_map(width, height, walls, blizzards, elf)
#         return None
#     if elf == stop:
#         print(f"FOUND solution at {steps} steps!!")
#         min_steps = steps
#         return steps        
#     if elf in walls or elf in blizzards:
#         return None
#     if elf in visited and visited[elf] > MAX_VISITS:
#         return None
#     distance = distance_between(elf, stop)
#     if steps + distance >= min_steps:
#         print("elf at", elf)
#         return None
#     if elf[1] <= 0 and steps > 0:
#         return None
#     # debug
#     # print_map(width, height, walls, blizzards, elf)
#     # input()
    
#     # track elf visits
#     visited.setdefault(elf, 0)
#     visited[elf] += 1    
#     # find neighbors
#     elf_x, elf_y = elf
#     neighbors = [
#         (elf_x - 1, elf_y),
#         (elf_x + 1, elf_y),
#         (elf_x, elf_y - 1),
#         (elf_x, elf_y + 1),
#     ]
#     neighbors_with_distance = []
#     for neighbor in neighbors:
#         distance = distance_between(neighbor, stop)
#         neighbors_with_distance.append((neighbor, distance))
#     neighbors_with_distance.sort(key=lambda item: item[1])

#     new_blizzards = move_blizzards(blizzards, walls)    
#     steps += 1
#     results = []    
#     # check adjacent positions and move elf
#     # did_find_ground = False
#     for neighbor, _ in neighbors_with_distance:
#         temp = dfs_search(neighbor, stop, new_blizzards, walls, width, height, steps)        
#         if temp is not None:
#             results.append(temp)
#             # did_find_ground = True
#     # if not did_find_ground:
#     # make elf wait        
#     temp = dfs_search(elf, stop, new_blizzards, walls, width, height, steps)
#     if temp:
#         results.append(temp)
#     # results = [x for x in results if x is not None]
#     if results:
#         return min(results)
#     return None
        

walls = set()
blizzards = {}
valley = []

try:
    filename = str(sys.argv[1])
except Exception as e:
    print("Warning exception:", e)
    filename = "sample2"
# assert filename == "input" or filename == "sample"
filename += ".txt"

with open(filename, "r") as handle:    
    for y, line in enumerate(handle):
        line = line.strip()
        valley.append(line)
        for x, ch in enumerate(line):
            if ch == WALL:
                walls.add((x, y))
            elif ch == GROUND:
                continue
            elif ch in BLIZZARD:
                blizzards.setdefault((x, y), set())
                blizzards[(x, y)].add(ch)
                # blizzards.append([ch, x, y])
                # blizz_set.add((x, y))

WIDTH = len(valley[0])
HEIGHT = len(valley)
start = (1, 0)
stop = (WIDTH - 2, HEIGHT - 1)
print(f"width: {WIDTH}, height: {HEIGHT}")
print_map(WIDTH, HEIGHT, walls, blizzards, start)

# DEBUG
blizzards_copy = deepcopy(blizzards)
for _ in range(20):
    print_map(WIDTH, HEIGHT, walls, blizzards_copy, start, to_file=True)
    blizzards_copy = move_blizzards(blizzards_copy, walls)
# DEBUG

# for i in range(10):
#     blizzards = move_blizzards(blizzards, walls)
#     print_map(WIDTH, HEIGHT, walls, blizzards)
#     input("press enter to continue..")

distances = bfs_search(start, stop, blizzards, walls, WIDTH, HEIGHT)
print(distances)
stop_x, stop_y = stop
answer = distances[stop_y][stop_x]
print(answer)

# answer = dfs_search(start, stop, blizzards, walls, WIDTH, HEIGHT, 0)
# print("Min distance:", distance_between(start, stop))
# print("Result:", answer)
if filename == "sample.txt":
    assert answer == 18

# 1019, 1011, 557, 631 too high
# 485 not sent