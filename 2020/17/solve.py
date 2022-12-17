import itertools


def add_delta(coordinate, delta):
    new_coord = []
    for i in range(len(coordinate)):
        new_coord.append(coordinate[i] + delta[i])
    return tuple(new_coord)


def is_origin(coordinate):
    for i in coordinate:
        if i != 0:
            return False
    return True


def simulate_cycle(states, dimensions):
    coordinate_values = []
    for i in range(dimensions):
        coordinate_values.append([s[i] for s in states])

    coordinate_ranges = []
    for i in range(dimensions):
        temp = list(range(min(coordinate_values[i]) - 1, max(coordinate_values[i]) + 2))
        coordinate_ranges.append(temp)

    # https://stackoverflow.com/questions/3034014/how-to-apply-itertools-product-to-elements-of-a-list-of-lists
    # https://stackoverflow.com/questions/400739/what-does-asterisk-mean-in-python
    coordinates = itertools.product(*coordinate_ranges)

    # Iterate through all cubes, save all new active states
    new_states = set()
    for c in coordinates:
        # Iterate through all neighbors, count active neighbors
        neighbors = 0
        for delta in itertools.product([-1, 0, 1], repeat=dimensions):
            if not is_origin(delta):  # e.g. if not (dx == dy == dz == 0):
                neighbor = add_delta(c, delta)
                if neighbor in states:
                    neighbors += 1
        # "If a cube is active and exactly 2 or 3 of its neighbors
        # are also active, the cube remains active. Otherwise,
        # the cube becomes inactive."
        if c in states and (neighbors == 2 or neighbors == 3):
            new_states.add(c)
        # "If a cube is inactive but exactly 3 of its neighbors are
        # active, the cube becomes active. Otherwise, the cube
        # remains inactive."
        if c not in states and neighbors == 3:
            new_states.add(c)

    return new_states


def parse_input(filename, dimensions):
    with open(filename, "r") as handle:
        puzzle_input = [line.strip() for line in handle]
    # for p in puzzle_input:
    #     print(p)
    active_states = set()
    for y, line in enumerate(puzzle_input):
        for x, state in enumerate(line):
            if state == "#":
                if dimensions == 3:
                    active_states.add((x, y, 0))
                if dimensions == 4:
                    active_states.add((x, y, 0, 0))
    # print(active_states)
    return active_states


def solve(filename, dimensions):
    assert dimensions in [3, 4]
    active_states = parse_input(filename, dimensions)

    for _ in range(6):
        active_states = simulate_cycle(active_states, dimensions)

    # print(active_states)
    # print(f"Active states: {len(active_states)}")
    return len(active_states)


# *****************
# Part 1
# *****************
part1_result1 = solve("sample.txt", 3)
part1_result2 = solve("input.txt", 3)

assert part1_result1 == 112
assert part1_result2 == 362

print(f"Part 1: {part1_result2} active states")

# *****************
# Part 2
# *****************
part2_result1 = solve("sample.txt", 4)
part2_result2 = solve("input.txt", 4)

assert part2_result1 == 848
assert part2_result2 == 1980


print(f"Part 2: {part2_result2} active states")
