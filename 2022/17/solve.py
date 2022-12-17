from copy import deepcopy
import hashlib

DASH = 0
PLUS = 1
LSHAPE = 2
ISHAPE = 3
SQUARE = 4

# X marks the base position

# ..X### DASH starts at (2, y)

# ...#.
# ..X##  PLUS (2, y)
# ...#.

# ....#
# ....#
# ..X##   LSHAPE (2, y)

# ..#
# ..#
# ..#
# ..X   ISHAPE also same

# ..##
# ..X#   SQUARE also same

shape_offsets = {
    DASH:   [(0, 0), (1, 0), (2, 0), (3, 0)],
    PLUS:   [(0, 0), (1, 0), (2, 0), (1, 1), (1, -1)],
    LSHAPE: [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    ISHAPE: [(0, 0), (0, 1), (0, 2), (0, 3)],
    SQUARE: [(0, 0), (1, 0), (0, 1), (1, 1)]
}

PLUS_SPECIAL_OFFSETS = [[0,0], [0,1], [0,2], [-1,1], [1,1]]

shape_heights = {
    DASH:   1,
    PLUS:   3,
    LSHAPE: 3,
    ISHAPE: 4,
    SQUARE: 2
}

falling_order = [DASH, PLUS, LSHAPE, ISHAPE, SQUARE]

CHAMBER_WIDTH = 7
FLOOR = "-"
ROCK = "#"
FLOATING_ROCK = "@"
DEBUG = False
ROCKS = list(map(str, [FLOOR, DASH, PLUS, LSHAPE, ISHAPE, SQUARE, ROCK]))

# def move_rock_left(pos):
#     x, y = pos
#     if x > 0:
#         return [x-1, y]
#     return pos


# def move_rock_right(rock, pos):
#     x, y = pos
#     if rock == DASH:
#         if x + 3 == CHAMBER_WIDTH - 1:
#             # do nothing
#             return pos
#         return [x+1, y]
#     if rock == PLUS or rock == LSHAPE:
#         if x + 2 == CHAMBER_WIDTH - 1:
#             return pos
#         return [x+1, y]
#     if rock == ISHAPE:
#         if x == CHAMBER_WIDTH - 1:
#             return pos
#         return [x+1, y]
def extend_chamber(chamber):
    chamber.extend(["."] * CHAMBER_WIDTH for _ in range(5))
    return chamber


def is_colliding(rock, position, chamber):
    offsets = shape_offsets[rock]
    for offset in offsets:
        x = position[0] + offset[0]
        y = position[1] + offset[1]
        if y >= len(chamber):
            chamber = extend_chamber(chamber)
        # print_chamber(chamber)
        # print("is_colliding", (x, y))
        if x < 0: # wall
            #print("IS COLLIDING WITH WALL")
            return True
        if x > CHAMBER_WIDTH - 1: # wall
            #print("IS COLLIDING WITH WALL")
            return True
        if chamber[y][x] in ROCKS: #== ROCK or chamber[y][x] == FLOOR:
            #print("IS COLLIDING WITH:", chamber[y][x])
            return True        
    return False


def print_section(chamber):
    chamber_copy = deepcopy(chamber)    
    for i in range(len(chamber_copy)-1, -1, -1):
        print(''.join(chamber_copy[i]))


def print_chamber(chamber, rock, position):
    if not DEBUG:
        return
    chamber_copy = deepcopy(chamber)
    for offset in shape_offsets[rock]:
        x = position[0] + offset[0]
        y = position[1] + offset[1]
        if y >= len(chamber):
            chamber_copy = extend_chamber(chamber_copy)
        chamber_copy[y][x] = FLOATING_ROCK        
    for i in range(len(chamber_copy)-1, -1, -1):
        print(''.join(chamber_copy[i]))
    input("press enter to continue..")


def verify_pattern(chamber, index1, index2):
    #print("VERIFYPATTERN", index1, index2)
    if index1 >= len(chamber) or index2 >= len(chamber):
        return False
    if chamber[index1] != chamber[index2]:
        return False
    assert index1 < index2
    offset = 1
    while index1 + offset < index2:
        if chamber[index1 + offset] != chamber[index2 + offset]:
            print("VERIFY_PATTERN FALSE:", index1, index2, offset, ''.join(chamber[index1 + offset]), " VS ", ''.join(chamber[index2 + offset]))
            return False
        offset += 1
    print("VERIFIED REPEATING SECTION:")
    #print_section(chamber[index1:index2])
    return True

def get_section_hash(section):
    section_str = ''.join([''.join(x) for x in section])
    return hashlib.md5(section_str.encode('utf-8')).hexdigest()


pattern_lookup = {} # { hash : (chamber_row_index, rocks_fallen) }
def search_for_pattern(chamber, rocks_fallen):
    pattern_len = 100
    chamber_height = calculate_height(chamber)
    for i in range(0, chamber_height - pattern_len, 1):
        section_hash = get_section_hash(chamber[i : i + pattern_len])
        # print("SECTION HASH", section_hash, "LOOKUP:", pattern_lookup, "CHAMBER HEIGHT:", chamber_height)
        section_info = (i, rocks_fallen)
        if section_hash not in pattern_lookup:
            pattern_lookup[section_hash] = section_info
        elif pattern_lookup[section_hash][0] != section_info[0]:
            print("PATTERN FOUND:", pattern_lookup[section_hash], "and", section_info)
            #print("At index", i)
            #print_section(chamber[i : i + pattern_len])
            index2, rocks2 = pattern_lookup[section_hash]
            #print("At index", index2)
            #print_section(chamber[index2 : index2 + pattern_len])
            if False:
            #if verify_pattern(chamber, index2, i):
                print("PATTERN VERIFIED!")
                # print_section(chamber[index2 : i])
                # print("OTHER SECTION:")
                # print_section(chamber[i : i + i - index2])
                # input()
            hash = get_section_hash(chamber[index2: i])
            actual_pattern_len = i - index2
            return (index2, actual_pattern_len, hash, rocks2, rocks_fallen, chamber[index2 : i])
            # print("PATTERN NOT VERIFIED: does not fully repeat between indices..")
            # input()
            
        
        # input()
    return None


def add_rock_to_chamber(rock, position, chamber):
    for offset in shape_offsets[rock]:
        x = position[0] + offset[0]
        y = position[1] + offset[1]
        if y >= len(chamber):
            chamber = extend_chamber(chamber)        
        chamber[y][x] = str(rock)
    return chamber


def calculate_height(chamber):
    for i in range(len(chamber)-1, -1, -1):
        for rock in ROCKS:
            if rock in chamber[i]:
                return i
    return 0


def calculate_section_height(section, rocks):
    # start from bottom of section
    section = deepcopy(section)
    print("CALCULATE SECTION HEIGHT BEFORE")
    print_section(section)
    rock_count = 0
    height = 0
    # loop through section, count up the rocks, count up the height
    for y_index, y in enumerate(section):
        for rock in [DASH, SQUARE, LSHAPE, ISHAPE, PLUS]:
            if str(rock) in y:
                x = y.index(str(rock))
                offsets = shape_offsets[rock]
                if rock == PLUS:
                    offsets = PLUS_SPECIAL_OFFSETS
                for offset in offsets:
                    offx, offy = offset
                    # print("offsets", offx, offy, x, y_index, ROCK)
                    section[y_index+offy][x+offx] = ROCK
                rock_count += 1
        if rock_count == rocks:
            break
    for y in section:
        if ROCK in y:
            height += 1            
    print("CALCULATE SECTION HEIGHT AFTER")
    print_section(section)
    print("HEIGHT:", height)
    return height
        

    for rock_index in range(rocks):
        while True:
            if (rock_index % 5) in section[row_index]:
                rock_index += 1
                rock_count += 1
        rock_index %= 5
    return 

heights = {} # { rock_index : height }

def solve(filename, num_rocks):
    with open(filename, "r") as handle:
        for line in handle:
            jet_pattern = line.strip()

    # num_jets = len(jet_pattern)
    # num_shapes = len(falling_order)
    # pattern_restart_index = num_jets * num_shapes
    # num_rocks_adjusted = num_rocks
    # print("num jets", num_jets)
    # if num_rocks > pattern_restart_index:
    #     multiplicand = num_rocks // pattern_restart_index
    #     num_rocks_adjusted = num_rocks % pattern_restart_index + pattern_restart_index        
    #     print("num rocks", num_rocks, ">", num_rocks_adjusted)    
    #     print("restart index", pattern_restart_index)
    #     print("multiplicand", multiplicand)
    #     input()

    pattern_rock_index = -1

    LEFT = "<"
    # RIGHT = ">"
    jet_index = 0
    height = 0
    chamber = []
    chamber.append(["-"] * CHAMBER_WIDTH)
    for i in range(num_rocks):
        # spawn rock
        # Each rock appears so that its left edge is two units away from the left wall 
        # and its bottom edge is three units above the highest rock in the room 
        # (or the floor) 
        rock = falling_order[i % len(falling_order)]
        extra = 1 if rock == PLUS else 0
        height = calculate_height(chamber)
        position = [2, height + 4 + extra]
        # print("SPAWN ROCK:")        
        # print_chamber(chamber, rock, position)

        while True:
            # apply jet pattern and move down until rock stops
            direction = jet_pattern[jet_index % len(jet_pattern)]
            jet_index += 1
            if direction == LEFT:
                #print("MOVE LEFT")
                position[0] -= 1
                if is_colliding(rock, position, chamber):
                    position[0] += 1
                print_chamber(chamber, rock, position)
            else:
                #print("MOVE RIGHT:")
                position[0] += 1
                if is_colliding(rock, position, chamber):
                    position[0] -= 1
                print_chamber(chamber, rock, position)
            # move rock down
            #print("MOVE DOWN:")
            position[1] -= 1
            if is_colliding(rock, position, chamber):
                position[1] += 1
                chamber = add_rock_to_chamber(rock, position, chamber)
                height = calculate_height(chamber)
                heights[i] = height
                print_chamber(chamber, rock, position)
                result = search_for_pattern(chamber, rocks_fallen=i)                
                # return (index2, actual_pattern_len, hash, rocks2, rocks_fallen)                
                if result:
                    _, actual_pattern_len, _, r1, r2, section = result
                    rock_pattern_length = r2-r1
                    print("PATTERN REPEATS BETWEEN rock #s:", r1, "and", r2, "pattern length", actual_pattern_len, ". Rock pattern length", rock_pattern_length)
                    # for remaining steps:
                    remaining_rocks = num_rocks - i - 1
                    multiplicand = remaining_rocks // (rock_pattern_length)
                    remainder = remaining_rocks % (rock_pattern_length)
                    
                    print("h", height, "num rocks:", num_rocks, "i:", i, "rpl:", rock_pattern_length, "mult:", multiplicand, "re:",remainder)
                    height += actual_pattern_len * (multiplicand)
                    remainder_height = heights[r1 + remainder] - heights[r1]
                    print("REMAINDER HEIGHT", remainder_height)
                    height += remainder_height # height += calculate_section_height(section, remainder)                    
                    print("CALCULATED HEIGHT", height)
                    return height
                    # return height
                    # pattern about to restart on next round
                    # TODO: STOPPED HERE. take the repeating pattern apply the maths and return the result
                    # input("press enter to continue..")
                break
            print_chamber(chamber, rock, position)
    return height
    # result = search_for_pattern(chamber)
    # if result:
    #     y1, y2 = result
    #     pattern_len = y2 - y1 + 1



    final_height = calculate_height(chamber)
    # TODO: final_height = pattern_height * (multiplicand - 1) + final_height
    print(num_rocks,":", final_height)
    return final_height


assert solve("sample2.txt", 30) == 26 * 3
assert solve("sample2.txt", 20) == 26 * 2
assert solve("sample2.txt", 10) == 26
assert solve("sample2.txt", 1000000) == 26 * 100000
assert solve("sample2.txt", 3) == 7
pattern_lookup = {}
heights = {}
assert solve("sample.txt", 1000000000000) == 1514285714288
assert solve("sample.txt", 40) == 66
assert solve("sample.txt", 80) == 125
assert solve("sample.txt", 2022) == 3068
pattern_lookup = {}
heights = {}
# PATTERN FOUND: (2052, 1408) and (4806, 3148)
# PATTERN FOUND: (351, 341) and (3105, 3149)
assert solve("input.txt", 2022) == 3219
assert solve("input.txt", 1000000000000) == 1582758620701
# solve(1000000000000)
