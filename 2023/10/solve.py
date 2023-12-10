import numpy as np

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn'

# example
# .....
# .S-7.
# .|.|.
# .L-J.
# .....

N = np.array([ 0, -1])
E = np.array([ 1,  0]) 
S = np.array([ 0,  1]) 
W = np.array([-1,  0])

def get_next_dest(start, dest, pipemap):
    dir = dest - start
    dx, dy = dest
    destpipe = pipemap[dy][dx]
    if destpipe == "|" and np.array_equal(dir, N): # facing north
        return dest + N
    if destpipe == "|" and np.array_equal(dir, S): # facing south
        return dest + S
    if destpipe == "-" and np.array_equal(dir, E): # facing east
        return dest + E
    if destpipe == "-" and np.array_equal(dir, W): # facing west        
        return dest + W
    if destpipe == "L" and np.array_equal(dir, W):
        return dest + N
    if destpipe == "L" and np.array_equal(dir, S):
        return dest + E
    if destpipe == "J" and np.array_equal(dir, E):
        return dest + N
    if destpipe == "J" and np.array_equal(dir, S):
        return dest + W
    if destpipe == "7" and np.array_equal(dir, E):
        return dest + S
    if destpipe == "7" and np.array_equal(dir, N):
        return dest + W
    if destpipe == "F" and np.array_equal(dir, W):
        return dest + S
    if destpipe == "F" and np.array_equal(dir, N):
        return dest + E

def printmap(mymap):
    for row in mymap:
        print("".join(row))

def is_path_available(start, destination, pipemap):
    sx, sy = start
    dx, dy = destination
    destpipe = pipemap[dy][dx]
    if dy - sy == -1:
        # going north
        return destpipe in ["|", "7", "F"]
    if dy - sy == 1:
        # going south
        return destpipe in ["|", "L", "J"]
    if dx - sx == 1:
        # going east
        return destpipe in ["-", "J", "7"]
    if dx - sx == -1:
        # going west
        return destpipe in ["-", "F", "L"]
    assert False


def solve(filename, part2=False):
    with open(filename, "r", encoding="utf8") as handle:
        lines = handle.readlines()

    for y, line in enumerate(lines):
        if "S" in line:
            start = np.array([line.index("S"), y])
    
    pipemap = [line.strip() for line in lines]
    print(start)

    # start search north
    current = start
    directions = [N, E, S, W]
    for startdir in directions:
        # try all four directions
        current = start
        dest = start + startdir
        print("DEST", dest)
        if not is_path_available(current, dest, pipemap):
            continue

        # pipeline set for part 2
        pipeline = []
        pipeline.append(tuple(start))
        pipeline.append(tuple(dest))
        # need to get off the "S" square
        next_dest = get_next_dest(current, dest, pipemap)
        pipeline.append(tuple(next_dest)) # part 2
        current = dest
        dest = next_dest
        
        found_loop = False
        steps = 1
        while is_path_available(current, dest, pipemap):
            next_dest = get_next_dest(current, dest, pipemap)
            pipeline.append(tuple(next_dest)) # part 2
            current = dest
            dest = next_dest
            steps += 1
            if np.array_equal(current, "S"):
                # made it through the loop
                found_loop = True
                break
        if found_loop:
            break
    print("made it", steps)
    print("pipeline", pipeline)

    part1 = (steps + 1) // 2
    print("part1", part1)

    # part 2
    newmap = []
    for row in pipemap:
        newmap.append(["."]*len(row))
    for x, y in pipeline:
        newmap[y][x] = pipemap[y][x]
    printmap(newmap)
    
    tempmap = []
    for row in newmap:
        temprow = []
        newrow = []
        for pipe in row:
            if pipe == "S":
                # WARNING: shortcut/hack to follow
                # definitely the wrong way to find pipe value of "S"
                if "input.txt" in filename:
                    pipe = "J"
                elif "sample" in filename:
                    pipe = "F"
            if pipe == ".":
                temprow.extend([".","."])
                newrow.extend( [".","."])
            elif pipe == "|":
                temprow.extend(["|","."])
                newrow.extend( ["|","."])
            elif pipe == "-":
                temprow.extend(["-","-"])
                newrow.extend( [".","."])
            elif pipe == "L":
                temprow.extend(["L","-"])
                newrow.extend( [".","."])
            elif pipe == "J":
                temprow.extend(["J","."])
                newrow.extend( [".","."])
            elif pipe == "7":
                temprow.extend(["7","."])
                newrow.extend( ["|","."])
            elif pipe == "F":
                temprow.extend(["F","-"])
                newrow.extend( ["|","."])
        tempmap.append(temprow)
        tempmap.append(newrow)
    
    newmap = tempmap
    printmap(newmap)
    
    assert (0, 0) not in pipeline
    outside = set()
    queue = [(0, 0)]
    while queue:
        pos = queue.pop(0)
        # check bounds
        if pos[0] < 0 or pos[0] >= len(newmap[0]):
            continue
        # allow y to go to -1 for flood checking
        if pos[1] < -1 or pos[1] >= len(newmap):
            continue
        if pos in outside:
            continue
        # make an exception for -1
        if pos[1] == -1:
            pass
        elif newmap[pos[1]][pos[0]] != ".":
            continue

        outside.add(pos)

        north = tuple(np.array(list(pos)) + N)
        east  = tuple(np.array(list(pos)) + E)
        south = tuple(np.array(list(pos)) + S)
        west  = tuple(np.array(list(pos)) + W)
        queue.extend([north, east, south, west])
    print("outside", outside)

    for x, y in outside:
        if y < 0:
            continue
        newmap[y][x] = "O"

    printmap(newmap)

    enclosed = 0
    for y, row in enumerate(newmap):
        if y % 2 == 1:
            # all the odd rows were added, therefore skip them
            continue
        for x, col in enumerate(row):
            if x % 2 == 1:
                # odd columns were added too; skip
                continue
            if col == ".":
                enclosed += 1
    part2 = enclosed

    print(f"Results: {part1}, {part2}")
    return part1, part2

    

def test(path):
    assert solve(path + "sample.txt") == (4, 1)
    assert solve(path + "sample2.txt") == (8, 1)
    assert solve(path + "sample3.txt") == (22, 4)
    assert solve(path + "input.txt") == (6613, 511)

if __name__ == "__main__":
    test("./")
