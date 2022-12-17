from copy import deepcopy

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
DEBUG = True

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
        if chamber[y][x] == ROCK or chamber[y][x] == FLOOR:
            #print("IS COLLIDING WITH:", chamber[y][x])
            return True        
    return False


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


def add_rock_to_chamber(rock, position, chamber):
    for offset in shape_offsets[rock]:
        x = position[0] + offset[0]
        y = position[1] + offset[1]
        if y >= len(chamber):
            chamber = extend_chamber(chamber)        
        chamber[y][x] = ROCK        
    return chamber


def calculate_height(chamber):
    for i in range(len(chamber)-1, -1, -1):
        if ROCK in chamber[i]:
            return i
    return 0


def solve(filename, num_rocks):
    with open(filename, "r") as handle:
        for line in handle:
            jet_pattern = line.strip()

    num_jets = len(jet_pattern)
    num_shapes = len(falling_order)
    pattern_restart_index = num_jets * num_shapes
    num_rocks_adjusted = num_rocks
    print("num jets", num_jets)
    if False: # num_rocks > pattern_restart_index:
        multiplicand = num_rocks // pattern_restart_index
        num_rocks_adjusted = num_rocks % pattern_restart_index + pattern_restart_index        
        print("num rocks", num_rocks, ">", num_rocks_adjusted)    
        print("restart index", pattern_restart_index)
        print("multiplicand", multiplicand)
        input()

    pattern_height = 0

    LEFT = "<"
    # RIGHT = ">"
    jet_index = 0
    chamber = []
    chamber.append(["-"] * CHAMBER_WIDTH)
    for i in range(num_rocks_adjusted):
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
                print_chamber(chamber, rock, position)
                break            
            print_chamber(chamber, rock, position)
        
        if i == pattern_restart_index:

            height = calculate_height(chamber)
            pattern_height = height

    final_height = calculate_height(chamber)
    # TODO: final_height = pattern_height * (multiplicand - 1) + final_height
    print(num_rocks,":", final_height)
    return final_height

# solve("sample.txt", 3000)
assert solve("sample.txt", 40) == 66
assert solve("sample.txt", 80) == 125
assert solve("sample.txt", 2022) == 3068
# assert solve("input.txt", 2022) == 3219
# solve(1000000000000)
