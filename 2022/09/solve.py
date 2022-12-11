import math

#  1 2 3
# 1 . . .
# 2 . x .
# 3 . . .


def is_tail_touching(head, tail):
    if head[0] - tail[0] == 0 and abs(head[1] - tail[1]) <= 1:
        return True
    if head[1] - tail[1] == 0 and abs(head[0] - tail[0]) <= 1:
        return True
    if abs(head[0] - tail[0]) == 1 and abs(head[1] - tail[1]) == 1:
        return True
    return False


def get_new_tail_position(head, tail):
    # # move straight
    # if abs(head[0] - tail[0]) == 2 and head[1] - tail[1] == 0:
    #     return [ (head[0] + tail[0]) // 2, tail[1] ]
    # if abs(head[1] - tail[1] == 2) and head[0] - tail[0] == 0:
    #     return [ tail[0], (head[1] + tail[1]) // 2 ]
    # # move diag
    if head[0] - tail[0] == 0:
        if head[1] > tail[1]:
            return [tail[0], tail[1] + 1]
        else:
            return [tail[0], tail[1] - 1]
    elif head[1] - tail[1] == 0:
        if head[0] > tail[0]:
            return [tail[0] + 1, tail[1]]
        else:
            return [tail[0] - 1, tail[1]]
    # move diag
    if head[0] > tail[0]:
        tail[0] += 1
    else:
        tail[0] -= 1
    if head[1] > tail[1]:
        tail[1] += 1
    else:
        tail[1] -= 1
    return tail.copy()
    # temp = [int(math.ceil((head[0] + tail[0]) / 2)), int(math.ceil((head[1] + tail[1]) / 2))]


def print_map(rope):
    mymap = ["*" * 35] * 35
    offset = 17
    for i, knot in enumerate(rope):
        x, y = knot[0] + offset, knot[1] + offset
        mymap[y] = mymap[y][:x] + str(i) + mymap[y][x+1:]
    for line in reversed(mymap):
        print(line)
    print()


def solve(filename):
    moves = []
    with open(filename, 'r', encoding="utf8") as handle:
        for line in handle:
            move = line.strip().split(" ")
            moves.append(move)

    # PART 1
    print(moves)
    #           x, y
    tail_path = [(0, 0)]
    tail_pos = [0, 0]
    head_pos = [0, 0]
    for move in moves:
        direction = move[0]
        count = int(move[1])
        # move direction
        index = 0
        step = 1
        if direction == "U" or direction == "D":
            index = 1
        if direction == "L" or direction == "D":
            step = -1
        for i in range(count):
            prev_head_pos = head_pos.copy()
            head_pos[index] += step
            if not is_tail_touching(head_pos, tail_pos):
                tail_pos = prev_head_pos.copy()
                tail_path.append(tuple(tail_pos))
                # print("tail",tail_path)

    unique_positions = set()
    print(tail_path)
    for pos in tail_path:
        unique_positions.add(pos)
    part1 = len(unique_positions)
    print("PART 1", part1)

    # PART 2
    print("*** PART 2")
    num_knots = 10
    tail_path = [(0, 0)]
    rope = [[0, 0] for x in range(num_knots)]
    for move in moves:
        direction = move[0]
        count = int(move[1])
        # move direction
        index = 0
        delta = 1
        if direction == "U" or direction == "D":
            index = 1
        if direction == "L" or direction == "D":
            delta = -1

        for step in range(count):
            rope[0][index] += delta
            # Apply updates to rest of rope
            for knot_index in range(num_knots - 1):
                if is_tail_touching(rope[knot_index], rope[knot_index+1]):
                    break
                # if not touching, update position
                rope[knot_index + 1] = get_new_tail_position(
                    rope[knot_index], rope[knot_index + 1])
                #rope_prev[knot_index+1] = rope[knot_index+1].copy()
                #rope[knot_index+1] = rope_prev[knot_index].copy()
                if knot_index + 1 == num_knots - 1:
                    tail_path.append(tuple(rope[knot_index + 1]))
            # print(rope)
            # print_map(rope)
            pause = 0

    unique_positions = set()
    print("tail path", tail_path)
    for pos in tail_path:
        unique_positions.add(pos)
    part2 = len(unique_positions)
    print("len", part2)
    return part1, part2


def test(path):
    part1, part2 = solve(path + "sample.txt")
    assert part1 == 13
    assert part2 == 1

    _, part2 = solve(path + "sample2.txt")
    assert part2 == 36

    part1, part2 = solve(path + "input.txt")
    assert part1 == 6503
    assert part2 == 2724


if __name__ == "__main__":
    test("./")
