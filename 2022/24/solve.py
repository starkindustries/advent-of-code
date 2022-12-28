import sys
import hashlib
from copy import deepcopy
import json


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
GREEN = '\033[92m'
END_COLOR = '\033[0m'

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
                row += GREEN + ELF + END_COLOR
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

blizzards_lookup = []
def get_all_blizzards(blizzards, walls):
    global blizzards_lookup
    blizzards_lookup.append(blizzards)
    for i in range(1000):
        blizzards = move_blizzards(blizzards, walls)
        blizzards_lookup.append(blizzards)


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


def bfs_search(start, stop, blizzards, walls, width, height, starting_blizzard):
    # prunes_by_visited = 0
    # prunes_by_distance = 0
    # prunes_by_steps = 0
    # prunes_by_waits = 0
    
    start_x, start_y = start
    queue = [(start_x, start_y, 0)]
    distances = []

    for _ in range(width * height):
        array = []
        for _ in range(height):
            array.append([-1 for _ in range(width)])
        distances.append(array)

    start_x, start_y = start
    # distances[0][start_y][start_x] = 0
    # max_visits = 100000
    # visited = {} 
    # distance_threshold = 10
    # min_distance = float("inf")
    count = 0
    # too_many_steps = 631
    # max_waits = 200
    # waited = {}

    while queue:
        count += 1
        elf_x, elf_y, steps = queue.pop(0)
        elf = elf_x, elf_y
                
        # print_map(width, height, walls, blizzards, elf)
        if count % 1000 == 0:
            print(count, width*height*height*width)
        # Prune        
        # if steps > too_many_steps:
        #     prunes_by_steps += 1
        #     continue
        blizzards = blizzards_lookup[steps + starting_blizzard]
        if elf in walls or elf in blizzards or elf_y >= HEIGHT or elf_y < 0 or elf_x < 0 or elf_x > width:
            continue

        if distances[steps][elf_y][elf_x] == -1:
            distances[steps][elf_y][elf_x] = steps
        else:
            continue

        if elf == stop:            
            return distances

        # if did_wait:
        #     waited.setdefault(elf, 0)
        #     waited[elf] += 1
        # visited.setdefault(elf, 0)
        # visited[elf] += 1
        # if elf in waited and waited[elf] > max_waits:
        #     prunes_by_waits += 1
        #     continue
        # if visited[elf] > max_visits:
        #     prunes_by_visited += 1
        #     continue            
        # distance = distance_between(elf, stop)
        # min_distance = distance if distance < min_distance else min_distance
        # if distance_between(elf, stop) > min_distance + distance_threshold:
        #     prunes_by_distance += 1
        #     continue

        # if count > 10000:
        #     count = 0
        #     print_map(width, height, walls, blizzards, elf)
        #     print((elf_x, elf_y), "distance to goal:", distance, "steps:", steps, "min_distance:", min_distance)
        #     if elf in waited:
        #         print("times waited:", waited[elf])
        #     print("prunes. visits:", prunes_by_visited, "distance:", prunes_by_distance, "steps:", prunes_by_steps, "waits:", prunes_by_waits)
        #     print("max visited:", max([val for _, val in visited.items()]))
        
        steps += 1
        # new_blizzards = move_blizzards(blizzards, walls)
        # print("steps", steps)
        # new_blizzards = blizzards_lookup[steps]
        neighbors = [
            (elf_x - 1, elf_y, steps),
            (elf_x + 1, elf_y, steps),
            (elf_x, elf_y - 1, steps),
            (elf_x, elf_y + 1, steps),
            (elf_x, elf_y, steps)
        ]        
        # move
        for neighbor in neighbors:
            # did_wait = False
            # nx, ny, steps = neighbor
            queue.append(neighbor)
        # wait
        # if steps >= 1 and elf_y > 0:
        #     did_wait = True
        # queue.append(elf_x, elf_y, steps)
            # queue.append((elf, new_blizzards, steps, did_wait))
    # print("prunes. visits:", prunes_by_visited, "distance:", prunes_by_distance, "steps:", prunes_by_steps, "waits:", prunes_by_waits)
    # print("max visited:", max([val for _, val in visited.items()]))
    return distances


def distance_between(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x2 - x1) + abs(y2 - y1)


def get_min_distance(position, distances):
    stop_x, stop_y = position
    min_steps = float("inf")
    for state in distances:    
        steps = state[stop_y][stop_x]
        if steps != -1:
            min_steps = min(min_steps, steps)
    return min_steps

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
    filename = "sample"
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

get_all_blizzards(blizzards, walls)
# DEBUG
# blizzards_copy = deepcopy(blizzards)
# blizzards_original = deepcopy(blizzards)
# for _ in range(20):
#     print_map(WIDTH, HEIGHT, walls, blizzards_copy, start, to_file=True)
#     blizzards_copy = move_blizzards(blizzards_copy, walls)
# DEBUG

# for i in range(10):
#     blizzards = move_blizzards(blizzards, walls)
#     print_map(WIDTH, HEIGHT, walls, blizzards)
#     input("press enter to continue..")

distances = bfs_search(start, stop, blizzards, walls, WIDTH, HEIGHT, 0)
answer1 = get_min_distance(stop, distances)
print(answer1)

# answer = dfs_search(start, stop, blizzards, walls, WIDTH, HEIGHT, 0)
# print("Min distance:", distance_between(start, stop))
# print("Result:", answer)
if filename == "sample.txt":
    assert answer1 == 18
if filename == "sample2.txt":
    assert answer1 == 20
if filename == "input.txt":
    assert answer1 == 257

# 1019, 1011, 557, 631 too high
# 485 not correct

# Part 2
distances = bfs_search(stop, start, blizzards, walls, WIDTH, HEIGHT, answer1)
answer2 = get_min_distance(start, distances)
print(answer2)

distances = bfs_search(start, stop, blizzards, walls, WIDTH, HEIGHT, answer1 + answer2)
answer3 = get_min_distance(stop, distances)
print(answer3)
print("part 2:", answer1, answer2, answer3, "sum:", sum([answer1, answer2, answer3]))