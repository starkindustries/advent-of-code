

ELF = "#"
GROUND = "."
elves = set()


def print_map():
    count = 0
    max_x = max(elves, key=lambda coord:coord[0])[0]
    max_y = max(elves, key=lambda coord:coord[1])[1]
    min_x = min(elves, key=lambda coord:coord[0])[0]
    min_y = min(elves, key=lambda coord:coord[1])[1]
    for y in range(min_y, max_y+1, 1):
        row = ""
        for x in range(min_x, max_x + 1, 1):
            if (x, y) in elves:
                row += ELF
            else:
                count += 1
                row += GROUND
        print(row)
    return count


def is_elf_at_location(position, offset, elves):
    x, y = position
    dx, dy = OFFSETS[offset]
    new_x, new_y = x + dx, y + dy
    if (new_x, new_y) in elves:
        return True
    return False


def add_offset(coords, offset):
    x, y = coords
    dx, dy = OFFSETS[offset]
    return (x + dx, y + dy)


filename = "input.txt"
with open(filename, "r") as handle:
    for y, line in enumerate(handle):
        line = line.strip()
        for x, ch in enumerate(line):
            if ch == ELF:
                elves.add((x, y))

print_map()
print()

NW = 0
N = 1
NE = 2
W = 3
E = 4
SW = 5
S = 6
SE = 7

OFFSETS = {
    NW: (-1, -1), # NW
    N:  ( 0, -1), # N
    NE: ( 1, -1), # NE
    W:  (-1,  0), # W
      # ( 0,  0), # POSITION
    E:  ( 1,  0), # E
    SW: (-1,  1), # SW
    S:  ( 0,  1), # S
    SE: ( 1,  1), # SE
}

proposal_directions = [
    (N, NW, NE),
    (S, SE, SW),
    (W, NW, SW),
    (E, NE, SE)
]

round = 0
while True:
    elf_proposals = {} # location : [elf]
    all_elves_do_nothing = True
    # first half
    for elf in elves:
        x, y = elf
        do_nothing = True
        for direction in OFFSETS:
            if is_elf_at_location(elf, direction, elves):
                do_nothing = False
        if do_nothing:
            continue
        all_elves_do_nothing = False
        for proposal in proposal_directions:
            elf_found = False
            for direction in proposal:
                if is_elf_at_location(elf, direction, elves):
                    elf_found = True
                    break
            if not elf_found:
                location = add_offset(elf, proposal[0])
                elf_proposals.setdefault(location, [])
                elf_proposals[location].append(elf)
                break
    if all_elves_do_nothing:
        part2 = round + 1
        break
    # second half
    for location, proposee in elf_proposals.items():
        if len(proposee) > 1:
            continue    
        elves.remove(proposee[0])
        elves.add(location)

    # End of round, rotate proposals
    item = proposal_directions.pop(0)
    proposal_directions.append(item)

    if round == 9:
        part1 = print_map()

    round += 1
    # print("ROUND", round + 1)
    # print_map()
    # input("press enter to continue..")
    
# part1 = print_map()
print("PART 1", part1)
print("PART 1", part2)
# PART 1 4070
# PART 1 881


"""
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""
