import functools
from copy import deepcopy

filename = "sample.txt"
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


TOP_EDGE = 0
RIGHT_EDGE = 1
BOTTOM_EDGE = 2
LEFT_EDGE = 3
EDGE_STRINGS = {
    TOP_EDGE: "TOP", 
    RIGHT_EDGE: "RIGHT",
    BOTTOM_EDGE: "BOTTOM",
    LEFT_EDGE: "LEFT"
}
def print_squares(squares):
    # squares = {} # (x, y) => square_template
    for section, edges in squares.items():
        print(section)
        for name, edge in edges.items():
            print(f"  {EDGE_STRINGS[name]}: {edge}")


##############################
position = map[0].index('.')
position = (position, 0)

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
NUM_DIRECTIONS = 4
LEFT_TURN = "L"
RIGHT_TURN = "R"

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



# PART 2
SIDE_LEN = 4
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
for _ in range(20):
    for square, edges in squares.items():
        if len(edges) < 2:
            continue
        x, y = square
        #   X       X          X 0       0 X   
        # X 0       0 X          X       X
        # TOP/LEFT, TOP/RIGHT, BOT/LEFT, BOT/RIGHT
        corners = [
            (TOP_EDGE, LEFT_EDGE, 0, DOWN, 0, RIGHT),
            (TOP_EDGE, RIGHT_EDGE, 1, DOWN, 1, LEFT),
            (BOTTOM_EDGE, LEFT_EDGE, 1, UP, 1, RIGHT),
            (BOTTOM_EDGE, RIGHT_EDGE, 0, UP, 0, LEFT)
        ]
        for corner in corners:
            edge1, edge2, e1_flip, e1_dir, e2_flip, e2_dir = corner
            if edges[edge1] and edges[edge2]:
                e1_tuple = edges[edge1]
                e2_tuple = edges[edge2]
                e1_coord, _, _ = e1_tuple
                e2_cord, _, _ = e2_tuple            
                # print("**", top_edge, lcoord, 0, DOWN)
                # input()
                squares[e1_tuple[0]][edge2] = (e2_cord, e1_flip, e1_dir)
                squares[e2_tuple[0]][edge1] = (e1_coord, e2_flip, e2_dir)

print("\nsquares")
print_squares(squares)

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

