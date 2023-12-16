# directions
N, E, S, W = 0, 1, 2, 3

def calculate_energized(start, tilemap):
    assert isinstance(start, tuple)
    beams = [start]
    beam_path = set()
    while beams:
        b = beams.pop(0)
        if b in beam_path:
            continue
        beam_path.add(b)
        x, y, dir = b
        if dir == E:
            x2, y2 = x+1, y
            if x2 >= len(tilemap[0]):
                # out of bounds
                continue
            next = tilemap[y2][x2]
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
            next = tilemap[y2][x2]
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
            next = tilemap[y2][x2]
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
            if y2 >= len(tilemap):
                continue
            next = tilemap[y2][x2]
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
    return len(energized)

def solve(filename, part2=False):
    with open(filename, "r", encoding="utf8") as handle:
        lines = [line.strip() for line in handle.readlines()]

    # part1
    energized = calculate_energized((-1, 0, E), lines)

    # part2
    energies = []
    for x in range(len(lines[0])):
        e1 = calculate_energized((x, 0, S), lines) # top row
        e2 = calculate_energized((x, len(lines)-1, N), lines) # bottom row
        energies.extend([e1, e2])
    for y in range(len(lines)):
        e1 = calculate_energized((0, y, E), lines) # left column
        e2 = calculate_energized((len(lines[0])-1, y, W), lines) # right column
        energies.extend([e1, e2])    

    max_energy = max(energies)

    part1, part2 = energized, max_energy
    print(part1, part2)
    return part1, part2


def test(path):

    assert solve(path + "sample.txt") == (46, 51)
    assert solve(path + "input.txt") == (8112, 8314)

if __name__ == "__main__":
    test("./")
