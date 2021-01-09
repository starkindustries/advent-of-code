import itertools


# def get_neighbors(state, active_states, is_active):
#     x, y, z = state
#     diff = [-1, 0, 1]
#     neighbors = []
#     for xd in diff:
#         for yd in diff:
#             for zd in diff:
#                 if not (xd == yd == zd == 0):
#                     neighbor = (x+xd, y+yd, z+zd)
#                     if (neighbor in active_states) == is_active:
#                         neighbors.append(neighbor)
#     return neighbors


# def active_neighbors(state, active_states):
#     return get_neighbors(state, active_states, True)


# def inactive_neighbors(state, active_states):
#     return get_neighbors(state, active_states, False)


# def find_intersecting_neighbors(three_states, active_states):
#     s1 = inactive_neighbors(three_states[0], active_states)
#     s2 = inactive_neighbors(three_states[1], active_states)
#     s3 = inactive_neighbors(three_states[2], active_states)
#     return set(s1) & set(s2) & set(s3)


def simulate_cycle(states, dimensions):
    # assert dimensions in [3, 4]


    # for i in range(dimensions):
    x_values = [s[0] for s in states]
    y_values = [s[1] for s in states]
    z_values = [s[2] for s in states]

    x_range = range(min(x_values)-1, max(x_values)+2)
    y_range = range(min(y_values)-1, max(y_values)+2)
    z_range = range(min(z_values)-1, max(z_values)+2)

    coordinates = itertools.product(x_range, y_range, z_range)

    # Iterate through all cubes, save all new active states
    new_states = set()
    for x, y, z in coordinates:
        # Iterate through all neighbors, count active neighbors
        neighbors = 0
        for dx, dy, dz in itertools.product([-1, 0, 1], repeat=3):
            if not (dx == dy == dz == 0):
                if (x+dx, y+dy, z+dz) in states:
                    neighbors += 1
        # If a cube is active and exactly 2 or 3 of its neighbors
        # are also active, the cube remains active. Otherwise,
        # the cube becomes inactive.
        if (x, y, z) in states and (neighbors == 2 or neighbors == 3):
            new_states.add((x, y, z))
        # If a cube is inactive but exactly 3 of its neighbors are
        # active, the cube becomes active. Otherwise, the cube
        # remains inactive.
        if (x, y, z) not in states and neighbors == 3:
            new_states.add((x, y, z))

    return new_states

    # print("********* STARTING SIMULATION *********")
    # new_states = set()
    # delete_states = set()
    # for state in states:
    #     # If a cube is active and exactly 2 or 3 of its neighbors
    #     # are also active, the cube remains active. Otherwise,
    #     # the cube becomes inactive.
    #     neighbors = active_neighbors(state, states)
    #     count = len(neighbors)
    #     print(f"neighbor count for {state}: {count}")
    #     if not (count == 2 or count == 3):
    #         delete_states.add(state)
    #     # If a cube is inactive but exactly 3 of its neighbors are
    #     # active, the cube becomes active. Otherwise, the cube
    #     # remains inactive.
    #     # If count is 2 plus the state itself makes 3 active states
    #     if count == 2:
    #         neighbors.append(state)
    #         print(f"neighbors: {neighbors}")
    #         intersection = find_intersecting_neighbors(neighbors, states)
    #         print(f"intersection: {intersection}")
    #         # verify that the intersection actually has 3 active neighbors
    #         for s in intersection:
    #             if active_neighbors(s, states) == 3:
    #                 new_states.add(s)

    # print(f"states to delete: {delete_states}")
    # states.difference_update(delete_states)

    # print(f"new states: {new_states}")
    # states.update(new_states)


def parse_input(filename, dimensions):
    assert dimensions in [3, 4]
    with open(filename, 'r') as handle:
        puzzle_input = [line.strip() for line in handle]
    for p in puzzle_input:
        print(p)
    active_states = set()
    for y, line in enumerate(puzzle_input):
        for x, state in enumerate(line):
            if state == "#":
                if dimensions == 3:
                    active_states.add((x, y, 0))
                if dimensions == 4:
                    active_states.add((x, y, 0, 0))
    print(active_states)
    return active_states


def solve_part1(filename):
    active_states = parse_input(filename, 3)

    for _ in range(6):
        active_states = simulate_cycle(active_states, 3)

    print(active_states)
    print(f"Active states: {len(active_states)}")
    return len(active_states)


assert solve_part1("sample.txt") == 112
assert solve_part1('input.txt') == 362

print(f"Part 1: {solve_part1('input.txt')} active states")
