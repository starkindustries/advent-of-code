# directions
N, E, S, W = 0, 1, 2, 3


def solve(filename, part2=False):
    with open(filename, "r", encoding="utf8") as handle:
        lines = [line.strip() for line in handle.readlines()]

    beam_path = set()
    beams = [(-1, 0, E)]
    while beams:
        b = beams.pop(0)
        if b in beam_path:
            continue
        beam_path.add(b)
        x, y, dir = b
        if dir == E:
            x2, y2 = x+1, y
            if x2 >= len(lines[0]):
                # out of bounds
                continue
            next = lines[y2][x2]
            if next == "|":
                beams.append((x2, y2, N))
                beams.append((x2, y2, S))
                continue
            elif next == "\\":
                beams.append((x2, y2, S))
                continue
            elif next == "/":
                beams.append((x2, y2, N))
                continue
            elif next == "-" or next == ".":
                beams.append((x2, y2, E))
                continue
        elif dir == W:
            x2, y2 = x-1, y
            if x2 < 0:
                continue
            next = lines[y2][x2]
            if next == "|":
                beams.append((x2, y2, N))
                beams.append((x2, y2, S))
                continue
            elif next == "\\":
                beams.append((x2, y2, N))
                continue
            elif next == "/":
                beams.append((x2, y2, S))
                continue
            elif next == "-" or next == ".":
                beams.append((x2, y2, W))
                continue
        elif dir == N:
            x2, y2 = x, y-1
            if y2 < 0:
                continue
            next = lines[y2][x2]
            if next == "|" or next == ".":
                beams.append((x2, y2, N))
                continue
            elif next == "\\":
                beams.append((x2, y2, W))
                continue
            elif next == "/":
                beams.append((x2, y2, E))
                continue  
            elif next == "-":
                beams.append((x2, y2, E))
                beams.append((x2, y2, W))
                continue
        elif dir == S:
            x2, y2 = x, y+1
            if y2 >= len(lines):
                continue
            next = lines[y2][x2]
            if next == "|" or next == ".":
                beams.append((x2, y2, S))
                continue
            elif next == "\\":
                beams.append((x2, y2, E))
                continue
            elif next == "/":
                beams.append((x2, y2, W))
                continue  
            elif next == "-":
                beams.append((x2, y2, E))
                beams.append((x2, y2, W))
                continue
    
    energized = set()
    for beam in beam_path:
        x, y, _ = beam
        if x == -1:
            continue # skip the start coordinate
        energized.add((x, y))

    part1, part2 = len(energized), 1
    print(part1, part2)
    return part1, part2


def test(path):

    assert solve(path + "sample.txt") == (46, 51)
    assert solve(path + "input.txt") # == (518107, 303404)

if __name__ == "__main__":
    test("./")
