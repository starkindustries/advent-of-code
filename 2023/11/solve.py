def printmap(mymap):
    for row in mymap:
        print("".join(row))

def solve(filename, expansion=2, part2=False):
    assert expansion > 1
    with open(filename, "r", encoding="utf8") as handle:
        lines = [line.strip() for line in handle.readlines()]

    empty_cols = [True] * len(lines[0])
    empty_rows = [True] * len(lines)
    for y, row in enumerate(lines):
        for x, col in enumerate(row):
            if col == "#":
                empty_cols[x] = False
                empty_rows[y] = False
    print(empty_cols)
    print(empty_rows)

    # get all galaxies
    galaxies = set()
    for y, row in enumerate(lines):
        for x, col in enumerate(row):
            if col == "#":
                galaxies.add((x, y))

    for y in range(len(empty_rows)-1, -1, -1):
        empty = empty_rows[y]
        if empty == True:
            to_remove = set()
            to_add = set()
            for g in galaxies:
                gx, gy = g
                assert gy != y
                if gy > y:
                    to_remove.add(g)
                    to_add.add((gx, gy+expansion-1))
            for g in to_remove:
                galaxies.remove(g)
            galaxies.update(to_add)
            
    for x in range(len(empty_cols)-1, -1, -1):
        empty = empty_cols[x]
        if empty == True:
            to_remove = set()
            to_add = set()
            for g in galaxies:
                gx, gy = g
                assert gx != x
                if gx > x:
                    to_remove.add(g)
                    to_add.add((gx+expansion-1, gy))
            for g in to_remove:
                galaxies.remove(g)
            galaxies.update(to_add)

    assert ((1, 2), (3, 4)) == ((1, 2), (3, 4))

    pairs = set()
    for g1 in galaxies:
        for g2 in galaxies:
            if (g1, g2) in pairs or (g2, g1) in pairs:
                continue
            pairs.add((g1, g2))
    
    print(pairs)
    total_distance = 0
    for p in pairs:
        g1, g2 = p
        dist = abs(g2[0] - g1[0]) + abs(g2[1] - g1[1])
        total_distance += dist

    print(f"Results: {total_distance=}, {expansion=}")
    return total_distance

    

def test(path):
    assert solve(path + "sample.txt", expansion=2)  == 374
    assert solve(path + "sample.txt", expansion=10) == 1030
    assert solve(path + "sample.txt", expansion=100) == 8410
    assert solve(path + "input.txt",  expansion=2)  == 9312968 # part1
    assert solve(path + "input.txt",  expansion=1000000) == 597714117556 # part2

if __name__ == "__main__":
    test("./")
