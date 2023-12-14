# directions
N, E, S, W = 0, 1, 2, 3

def roll_rocks(rockmap, spheres, squares, dir=N):
    if dir == N or dir == W:
        yrange = range(len(rockmap))
        xrange = range(len(rockmap[0]))
    if dir == S:
        yrange = range(len(rockmap)-1, -1, -1)
        xrange = range(len(rockmap[0]))
    if dir == E:
        yrange = range(len(rockmap))
        xrange = range(len(rockmap[0])-1, -1, -1)

    for y in yrange:
        for x in xrange:
            if (x, y) in spheres:
                spheres.remove((x, y))
                x2, y2 = x, y
                if dir == N:
                    while True:
                        if y2-1 < 0 or (x2, y2-1) in squares or (x2, y2-1) in spheres:
                            break
                        y2 -= 1
                elif dir == S:
                    while True:
                        if y2+1 >= len(rockmap) or (x2, y2+1) in squares or (x2, y2+1) in spheres:
                            break
                        y2 += 1
                elif dir == E:
                    while True:
                        if x2+1 >= len(rockmap[0]) or (x2+1, y2) in squares or (x2+1, y2) in spheres:
                            break
                        x2 += 1
                elif dir == W:
                    while True:
                        if x2-1 < 0 or (x2-1, y2) in squares or (x2-1, y2) in spheres:
                            break
                        x2 -= 1
                spheres.add((x2, y2))

def solve(filename, part2=False):
    with open(filename, "r", encoding="utf8") as handle:
        lines = [line.strip() for line in handle.readlines()]

    spheres = set()
    squares = set()
    for y, row in enumerate(lines):
        for x, col in enumerate(row):
            if col == "O":
                spheres.add((x, y))
            elif col == "#":
                squares.add((x, y))
    
    # part1
    spheres1 = spheres.copy()
    roll_rocks(lines, spheres1, squares, N)
        
    # calculate load
    load = 0
    num_rows = len(lines)
    for x, y in spheres1:
        load += num_rows - y
    part1 = load

    # part2
    spheres2 = spheres.copy()
    prev_spheres = []
    cycles = 1000000000
    found_pattern = False
    for i in range(cycles):
        roll_rocks(lines, spheres2, squares, N)
        roll_rocks(lines, spheres2, squares, W)
        roll_rocks(lines, spheres2, squares, S)
        roll_rocks(lines, spheres2, squares, E)

        for j, prev in enumerate(prev_spheres):
            if prev == spheres2:
                # cycles_to_go
                #               .-- total required cycles
                #               |        .-- # cycles already completed
                #               v        v          v-- # cycles in pattern
                cycles_to_go = (cycles - (i + 1)) % (i - j)
                spheres2 = prev_spheres[j + cycles_to_go]
                found_pattern = True
                break
        if found_pattern:
            break
        prev_spheres.append(spheres2.copy())

    # calculate load
    load = 0
    num_rows = len(lines)
    for x, y in spheres2:
        load += num_rows - y
    part2 = load

    print(part1, part2)
    return part1, part2


def test(path):
    assert solve(path + "sample.txt") == (136, 64)
    assert solve(path + "input.txt") == (106186, 106390)

if __name__ == "__main__":
    test("./")
