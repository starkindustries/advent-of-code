import functools
from copy import deepcopy


filename = "sample.txt"
filename = "input.txt"
get_instructions = False
map = []
history = []

def print_map(print_to_file=False):
    map_copy = deepcopy(map)
    for item in history:
        x, y, img = item
        map_copy[y][x] = img

    if not print_to_file:
        for row in map_copy:
            print(''.join(row) + "|") 
        return
    
    with open("map_printout.txt", "w", encoding="utf-8") as handle:
        for row in map_copy:
            handle.write(''.join(row) + "\n")

           


def get_first_number(instruction):
    assert instruction[0].isdigit()
    
    number = ''
    for ch in instruction:
        if ch.isdigit():
            number += ch
            continue        
        break
    new_instruction = instruction[len(number):]
    return (int(number), new_instruction)



with open(filename, "r") as handle:
    for line in handle:        
        if line.strip() == "":
            get_instructions = True
            continue
        if get_instructions:
            line = line.strip()
            instructions = line
            continue
        row = []
        for ch in line:
            if ch == "\n":
                continue
            row.append(ch)
        map.append(row)

print('012345678901234567890123456789')
# square off the map
WIDTH = len(max(map, key=lambda item: len(item)))
for row in map:
    gap = WIDTH - len(row)
    row.extend([' '] * gap)

print_map()
print(instructions)

HEIGHT = len(map)
OPEN = '.'
WALL = '#'
OFFMAP = " "
DIRECTION_IMG = ("^", ">", "v", "<") # up, right, down, left

#         ...#
#         .#..
#         #...
#         ....
# ...#.......#
# ........#...
# ..#....#....
# ..........#.
#         ...#....
#         .....#..
#         .#......
#         ......#.
@functools.lru_cache(maxsize=None)
def get_limit(coord, direction):
    x, y = coord
    if direction == RIGHT: # row stays the same
        for dx in range(WIDTH): # search left to right
            if map[y][dx] in [OPEN, WALL]:
                return (dx, y)
    if direction == LEFT:
        for dx in range(WIDTH-1, -1, -1): # search right to left
            if map[y][dx] in [OPEN, WALL]:
                return (dx, y)
    if direction == DOWN:
        for dy in range(HEIGHT): # search top to bottom
            if map[dy][x] in [OPEN, WALL]:
                return (x, dy)
    if direction == UP:
        for dy in range(HEIGHT-1, -1, -1): # search bottom to top
            if map[dy][x] in [OPEN, WALL]:
                return (x, dy)
    print("get_limit error: ", coord, direction)
    assert False


OFFSETS = [(0, -1), (1, 0), (0, 1), (-1, 0)] # up right down left
def move(position, steps, direction, map):
    x, y = position
    dx, dy = OFFSETS[direction]
    for _ in range(steps):
        
        if (y + dy < 0) or (y + dy >= HEIGHT) or (x + dx < 0) or (x + dx >= WIDTH) or map[y + dy][x + dx] == OFFMAP:
            lx, ly = get_limit((x, y), direction)
            if map[ly][lx] == WALL:
                return (x, y)
            x = lx
            y = ly
            history.append((x, y, DIRECTION_IMG[direction]))
            continue
        new_map_position = map[y + dy][x + dx]
        if new_map_position == WALL:
            return (x, y)
        elif new_map_position == OPEN:
            x += dx
            y += dy
            history.append((x, y, DIRECTION_IMG[direction]))
    return (x, y)

# directions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# edges
TOP_EDGE = 0
RIGHT_EDGE = 1
BOTTOM_EDGE = 2
LEFT_EDGE = 3
EDGE_STRINGS = {
    TOP_EDGE: "TOP_EDGE", 
    RIGHT_EDGE: "RIGHT_EDGE",
    BOTTOM_EDGE: "BOTTOM_EDGE",
    LEFT_EDGE: "LEFT_EDGE"
}
DIR_STRINGS = {
    RIGHT: "RIGHT",
    DOWN: "DOWN",
    LEFT: "LEFT",
    UP: "UP"
}
def print_squares(squares):
    # squares = {} # (x, y) => square_template
    print("squares = {")
    for section, edges in squares.items():
        print(f"{section}: {{")
        for name, edge in edges.items():
            if edge:
                coord = edge[0]
                flip = "FLIP" if edge[1] else "NO_FLIP"
                direction = DIR_STRINGS[edge[2]]
                print(f"  {EDGE_STRINGS[name]}: ({coord}, {flip}, {direction}),")
            else:
                print(f"  {EDGE_STRINGS[name]}: {edge},")
        print("},")
    print("}")

##############################
position = map[0].index('.')
position = (position, 0)


NUM_DIRECTIONS = 4
LEFT_TURN = "L"
RIGHT_TURN = "R"

instructions_part2 = instructions
direction = RIGHT
while True:
    if len(instructions) < 1:
        break
    # move a number of tiles
    steps, instructions = get_first_number(instructions)
    position = move(position, steps, direction, map)
    # print(steps, instructions)
    # turn 
    if len(instructions) < 1:
        break
    turn = instructions[0]
    instructions = instructions[1:]
    if turn == LEFT_TURN:
        direction = (direction - 1) % NUM_DIRECTIONS
    elif turn == RIGHT_TURN:
        direction = (direction + 1) % NUM_DIRECTIONS


# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
# r = 0, 1 = d, 2 = l, 3 = u
DIR_VALUES = {
    RIGHT: 0,
    DOWN: 1,
    LEFT: 2,
    UP: 3
}
x, y = position
x += 1
y += 1
# print_map(True)
print(x, y, DIR_VALUES[direction])
answer = 1000 * y + 4 * x + DIR_VALUES[direction]
print(answer)
if filename == "sample.txt":
    assert answer == 6032
if filename == "input.txt":
    assert answer == 11464
# 142300 - too high
# 11464 - correct



##############################
# PART 2
##############################
if filename == "sample.txt":
    SIDE_LEN = 4
elif filename == "input.txt":
    SIDE_LEN = 50
HORIZONTAL_SECTIONS = int(WIDTH / SIDE_LEN)
VERTICAL_SECTIONS = int(HEIGHT / SIDE_LEN)
sections = set()
for dy in range(VERTICAL_SECTIONS):
    for dx in range(HORIZONTAL_SECTIONS):    
        x = dx * SIDE_LEN
        y = dy * SIDE_LEN
        section_num = dy * SIDE_LEN + dx
        print(f"section:", section_num, (x, y))
        if map[y][x] in [WALL, OPEN]:
            print(f"section:", section_num, (x, y), "Active")
            sections.add((x, y))
        else:
            print(f"section:", section_num, (x, y))

print(sections)

squares = {} # (x, y) => square_template
square_template = { TOP_EDGE: None, RIGHT_EDGE: None, BOTTOM_EDGE: None, LEFT_EDGE: None}
index = 0


# OFFSETS = [(0, -1), (1, 0), (0, 1), (-1, 0)] # up right down left
for section in sections:
    x, y = section
    for direction, offset in enumerate(OFFSETS):
        dx, dy = offset
        dx *= SIDE_LEN
        dy *= SIDE_LEN
        side = (x + dx, y + dy)
        print("SIDE", side)
        if side not in sections: 
            continue           
        squares.setdefault(section, deepcopy(square_template))
        squares[section][direction] = ((x + dx, y + dy), 0, direction) # section, flip, facing_direction
        

#         X..# 
#         .#..
#         #...
#         ....
# ...#.......# 
# ........#...
# ..#....#....
# ..........#.
#         ...#....
#         .....#..
#         .#......
#         ......#.
# squares with two edges at non-opposite ends should join those edges to make a corner
# repeat this a couple times
for _ in range(1):
    for square, edges in squares.items():
        if len(edges) < 2:
            continue
        x, y = square
        #   X       X          X 0       0 X   
        # X 0       0 X          X       X
        # TOP/LEFT, TOP/RIGHT, BOT/LEFT, BOT/RIGHT
        corners = [
            # edge1, edge2, e1_flip, e1_dir, e2_flip, e2_dir
            (TOP_EDGE, LEFT_EDGE, 0, DOWN, 0, RIGHT),
            (TOP_EDGE, RIGHT_EDGE, 1, DOWN, 1, LEFT),
            (BOTTOM_EDGE, LEFT_EDGE, 1, UP, 1, RIGHT),
            (BOTTOM_EDGE, RIGHT_EDGE, 0, UP, 0, LEFT)
        ]
        for corner in corners:
            e1, e2, e1_flip, e1_dir, e2_flip, e2_dir = corner
            if edges[e1] and edges[e2]:
                e1_coord = edges[e1][0]
                e2_coord = edges[e2][0]
                # print("**", top_edge, lcoord, 0, DOWN)
                # input()
                if squares[e1_coord][e2] is None:
                    squares[e1_coord][e2] = (e2_coord, e1_flip, e1_dir)
                if squares[e2_coord][e1] is None:
                    squares[e2_coord][e1] = (e1_coord, e2_flip, e2_dir)
        # print("\nsquares")
        # print_squares(squares)
        # input()

print("\nsquares")
print_squares(squares)
print(squares)
# square sides = bottom north east south west top
# start from top-left-most active side. call this side bottom
# each side can travel to four other sides

# (8, 0) => UP:(0, 4, 180, DOWN), RIGHT:(8, 8, 180, LEFT), DOWN:(8, 4, 0, DOWN), LEFT:(4, 4, 90L,)
# 
# Flipped coordinate is just SIDE_LEN - index
#
#         X..# 
#         .#..
#         #...
#         ....
# ...#x......# 
# ........#...
# ..#....#....
# ..........#.
#         ...#....
#         .....#..
#         .#......
#         ......#.
# 
# section: 2 (8, 0) Active
# section: 3 (12, 0)
# section: 3 (12, 0)
# section: 4 (0, 4)
# section: 4 (0, 4) Active
# section: 5 (4, 4)
# section: 5 (4, 4) Active
# section: 6 (8, 4)
# section: 6 (8, 4) Active
# section: 7 (12, 4)
# section: 7 (12, 4)
# section: 8 (0, 8)
# section: 8 (0, 8)
# section: 9 (4, 8)
# section: 9 (4, 8)
# section: 10 (8, 8)
# section: 10 (8, 8) Active
# section: 11 (12, 8)
# section: 11 (12, 8) Active
NO_FLIP = 0
FLIP = 1

if filename == "sample.txt":
    SQUARES = {
        (4, 4): {
        TOP_EDGE: ((8, 0), NO_FLIP, RIGHT), # conf
        RIGHT_EDGE: ((8, 4), NO_FLIP, RIGHT), # conf
        BOTTOM_EDGE: ((8, 8), FLIP, RIGHT), # conf
        LEFT_EDGE: ((0, 4), NO_FLIP, LEFT), # conf
        },
        (8, 8): {
        TOP_EDGE: ((8, 4), NO_FLIP, UP), # conf
        RIGHT_EDGE: ((12, 8), NO_FLIP, RIGHT), # conf
        BOTTOM_EDGE: ((0, 4), FLIP, UP), # conf
        LEFT_EDGE: ((4, 4), FLIP, UP), # conf
        },
        (0, 4): {
        TOP_EDGE: ((8, 0), FLIP, DOWN), # conf
        RIGHT_EDGE: ((4, 4), NO_FLIP, RIGHT), # conf
        BOTTOM_EDGE: ((8, 8), FLIP, UP), # conf
        LEFT_EDGE: ((12, 8), FLIP, UP), # conf
        },
        (8, 4): {
        TOP_EDGE: ((8, 0), NO_FLIP, UP), # conf
        RIGHT_EDGE: ((12, 8), FLIP, DOWN), # conf
        BOTTOM_EDGE: ((8, 8), NO_FLIP, DOWN), # conf
        LEFT_EDGE: ((4, 4), NO_FLIP, LEFT), # conf
        },
        (8, 0): {
        TOP_EDGE: ((0, 4), FLIP, DOWN), # conf
        RIGHT_EDGE: ((12, 8), FLIP, LEFT), # conf
        BOTTOM_EDGE: ((8, 4), NO_FLIP, DOWN), # conf
        LEFT_EDGE: ((4, 4), NO_FLIP, DOWN), # conf
        },
        (12, 8): {
        TOP_EDGE: ((8, 4), FLIP, LEFT), # conf
        RIGHT_EDGE: ((8, 0), FLIP, LEFT), # conf
        BOTTOM_EDGE: ((0, 4), FLIP, RIGHT), # conf
        LEFT_EDGE: ((8, 8), NO_FLIP, LEFT), # conf
        },
    }

# use print squares to get partial edges
# print_squares()
# manual override
if filename == "input.txt":
    SQUARES = {
        (0, 100): {
        TOP_EDGE: ((50, 50), NO_FLIP, RIGHT), # conf
        # RIGHT_EDGE: ((50, 100), NO_FLIP, RIGHT), # conf
        # BOTTOM_EDGE: ((0, 150), NO_FLIP, DOWN), # conf
        LEFT_EDGE: ((50, 0), FLIP, RIGHT), # conf
        },
        (50, 100): {
        # TOP_EDGE: ((50, 50), NO_FLIP, UP), # conf
        RIGHT_EDGE: ((100, 0), FLIP, LEFT), # conf
        BOTTOM_EDGE: ((0, 150), NO_FLIP, LEFT), # conf
        # LEFT_EDGE: ((0, 100), NO_FLIP, DOWN), # conf
        },
        (50, 0): {
        TOP_EDGE: ((0, 150), NO_FLIP, RIGHT), # conf
        # RIGHT_EDGE: ((100, 0), NO_FLIP, RIGHT), # conf
        # BOTTOM_EDGE: ((50, 50), NO_FLIP, DOWN), # conf
        LEFT_EDGE: ((0, 100), FLIP, RIGHT), # conf
        },
        (100, 0): {
        TOP_EDGE: ((0, 150), NO_FLIP, UP), # conf
        RIGHT_EDGE: ((50, 100), FLIP, LEFT), # conf
        BOTTOM_EDGE: ((50, 50), NO_FLIP, LEFT), # conf
        # LEFT_EDGE: ((50, 0), NO_FLIP, LEFT), # conf
        },
        (0, 150): {
        # TOP_EDGE: ((0, 100), NO_FLIP, UP), # conf
        RIGHT_EDGE: ((50, 100), NO_FLIP, UP), # conf
        BOTTOM_EDGE: ((100, 0), NO_FLIP, DOWN), # conf
        LEFT_EDGE: ((50, 0), NO_FLIP, DOWN) # conf
        },
        (50, 50): {
        # TOP_EDGE: ((50, 0), NO_FLIP, UP), # conf
        RIGHT_EDGE: ((100, 0), NO_FLIP, UP), # conf
        # BOTTOM_EDGE: ((50, 100), NO_FLIP, DOWN), # conf
        LEFT_EDGE: ((0, 100), NO_FLIP, DOWN), # conf
        },
    }


history = []
def move2(position, steps, direction, map):
    x, y = position    
    for step in range(steps):
        dx, dy = OFFSETS[direction]
        new_x, new_y = x + dx, y + dy
        # if new position is out of bounds or off the map:
        if (new_y < 0) or (new_y >= HEIGHT) or (new_x < 0) or (new_x >= WIDTH) or map[new_y][new_x] == OFFMAP:            
            section = (x // SIDE_LEN * SIDE_LEN, y // SIDE_LEN * SIDE_LEN)
            print("SECTION: ", section, "x:", new_x, x, dx, "y:", new_y, y, dy)
            adjacent_edge, flip, facing_direction = SQUARES[section][direction]
            print(adjacent_edge, flip, facing_direction)
            if (direction in [UP, DOWN] and facing_direction in [LEFT, RIGHT]):
                # implement flipping from x to y
                edge_y = adjacent_edge[1] + (new_x % SIDE_LEN)
                if flip:
                    edge_y = adjacent_edge[1] + (SIDE_LEN - (new_x % SIDE_LEN) - 1)
                if facing_direction == LEFT:
                    edge_x = adjacent_edge[0] + SIDE_LEN - 1 # right edge of adjacent_edge, facing LEFT
                elif facing_direction == RIGHT:
                    edge_x = adjacent_edge[0] # left edge of adjacent_edge, facing RIGHT
            elif (direction in [LEFT, RIGHT] and facing_direction in [UP, DOWN]):
                # shifting direction 90 degrees, map y's to x's
                edge_x = adjacent_edge[0] + (new_y % SIDE_LEN)
                if flip:
                    edge_x = adjacent_edge[0] + (SIDE_LEN - (new_y % SIDE_LEN) - 1)
                if facing_direction == UP:
                    edge_y = adjacent_edge[1] + SIDE_LEN - 1 # bottom edge of adjacent_edge, facing UP
                elif facing_direction == DOWN:
                    edge_y = adjacent_edge[1] # top edge of adjacent_edge, facing DOWN
            elif direction in [LEFT, RIGHT] and facing_direction == LEFT:
                edge_y = adjacent_edge[1] + (new_y % SIDE_LEN)
                if flip:
                    edge_y = adjacent_edge[1] + (SIDE_LEN - (new_y % SIDE_LEN) - 1)
                edge_x = adjacent_edge[0] + SIDE_LEN - 1
            elif direction in [LEFT, RIGHT] and facing_direction == RIGHT:
                edge_y = adjacent_edge[1] + (new_y % SIDE_LEN)
                if flip:
                    edge_y = adjacent_edge[1] + (SIDE_LEN - (new_y % SIDE_LEN) - 1)
                edge_x = adjacent_edge[0]
            elif direction in [UP, DOWN] and facing_direction == UP:
                edge_x = adjacent_edge[0] + (new_x % SIDE_LEN)
                if flip:
                    edge_x = adjacent_edge[0] + (SIDE_LEN - (new_x % SIDE_LEN) - 1)
                edge_y = adjacent_edge[1] + SIDE_LEN - 1
            elif direction in [UP, DOWN] and facing_direction == DOWN:
                edge_x = adjacent_edge[0] + (new_x % SIDE_LEN)
                if flip:
                    edge_x = adjacent_edge[0] + (SIDE_LEN - (new_x % SIDE_LEN) - 1)
                edge_y = adjacent_edge[1]
            else:
                assert False

            if map[edge_y][edge_x] == WALL:
                return (x, y), direction
            x = edge_x
            y = edge_y
            direction = facing_direction
            history.append((x, y, DIRECTION_IMG[direction]))
            # print_map(True)
            # print(f"({x}, {y}), step {step} out of {steps}")
            # input("press enter to continue..")
            continue
        # If new position is within map bounds:
        new_map_position = map[y + dy][x + dx]
        if new_map_position == WALL:
            return (x, y), direction
        elif new_map_position == OPEN:
            x += dx
            y += dy
            history.append((x, y, DIRECTION_IMG[direction]))
        # print_map(True)
        # print(f"({x}, {y}), step {step} out of {steps}")
        # input("press enter to continue..")
    return (x, y), direction


def test_move(position, steps, direction, map, correct_pos, correct_dir):
    global history
    history = []
    ret_pos, ret_dir = move2(position, steps, direction, map)
    print("Given:", position, DIR_STRINGS[direction], "Results:", ret_pos, DIR_STRINGS[ret_dir], "Correct:", correct_pos, DIR_STRINGS[correct_dir])
    assert ret_pos == correct_pos
    assert ret_dir == correct_dir


#
#         1...2...  (50, 0), (100, 0)
#         ........
#         3...      (50, 50)
#         ....
#     4...5...      (0, 100), (50, 100)
#     ........
#     6...          (0, 150)
#     ....
#         


# Tests
history = []
# (50, 0)
test_move((50, 0), 1, UP, map, (0, 150), RIGHT)
test_move((99, 0), 1, UP, map, (0, 199), RIGHT)

test_move((50, 0), 1, LEFT, map, (0, 149), RIGHT)
test_move((50, 49), 1, LEFT, map, (0, 100), RIGHT)

# (100, 0)
test_move((100, 0), 1, UP, map, (0, 199), UP)
test_move((149, 0), 1, UP, map, (49, 199), UP)

test_move((149, 0), 1, RIGHT, map, (99, 149), LEFT)
test_move((149, 49), 1, RIGHT, map, (99, 100), LEFT)

test_move((100, 49), 1, DOWN, map, (99, 50), LEFT)
test_move((149, 49), 1, DOWN, map, (99, 99), LEFT)

# (50, 50)
test_move((50, 50), 1, LEFT, map, (0, 100), DOWN)
test_move((50, 99), 1, LEFT, map, (50, 99), LEFT) # hits wall
test_move((50, 98), 1, LEFT, map, (48, 100), DOWN) 

# (0, 100)
test_move((2, 100), 1, UP, map, (50, 52), RIGHT)
test_move((48, 100), 1, UP, map, (50, 98), RIGHT)

test_move((0, 100), 1, LEFT, map, (50, 49), RIGHT)
test_move((0, 149), 1, LEFT, map, (50, 0), RIGHT)

# (50, 100)
test_move((99, 100), 1, RIGHT, map, (149, 49), LEFT)
test_move((99, 149), 1, RIGHT, map, (149, 0), LEFT)

test_move((50, 149), 1, DOWN, map, (49, 150), LEFT)
test_move((99, 149), 1, DOWN, map, (49, 199), LEFT)

input("TEST COMPLETED..")
# exit()
# NUM_DIRECTIONS = 4  
# LEFT_TURN = "L"
# RIGHT_TURN = "R"

position = (map[0].index('.'), 0)
direction = RIGHT
instructions = instructions_part2
while True:
    if len(instructions) < 1:
        break
    # move a number of tiles
    print("steps:", steps)
    steps, instructions = get_first_number(instructions)
    print("steps:", steps, ", direction:", direction)
    position, direction = move2(position, steps, direction, map)
    # print(steps, instructions)
    # turn 
    if len(instructions) < 1:
        break
    turn = instructions[0]
    print("turn:", turn)
    instructions = instructions[1:]
    if turn == LEFT_TURN:
        direction = (direction - 1) % NUM_DIRECTIONS
    elif turn == RIGHT_TURN:
        direction = (direction + 1) % NUM_DIRECTIONS
    history.append((position[0], position[1], DIRECTION_IMG[direction]))

print_map(True)
x, y = position
x += 1
y += 1
print(x, y, DIR_VALUES[direction])
answer = 1000 * y + 4 * x + DIR_VALUES[direction]
print(answer)
if filename == "sample.txt":
    assert answer == 5031
    print("SUCCESS!!!", answer)
# 76360 too low
# 135120 too low
# 50486 no
# part2: 197122 YES!