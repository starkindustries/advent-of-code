

# Part 1
def parse_input(filename):
    temp_stacks = []
    moves = []
    get_stack = True
    columns = 0

    with open(filename, 'r', encoding="utf8") as handle:
        for line in handle:
            if line.strip() == "":
                get_stack = False
                continue
            if get_stack:
                if line[1].isdigit and line[1] == "1":
                    columns = list(map(int, line.split()))
                else:
                    temp_stacks.append(line)
            else:
                moves.append(line)

    # Parse stacks
    num_columns = columns[-1]
    stacks = [""] * num_columns
    stop = (num_columns - 1) * 4 + 1

    for x in range(len(temp_stacks)-1, -1, -1):
        # Get the boxes
        # 0123456789
        # [Z] [M] [P]
        # 1, 5, 9, 13,
        col = 0
        for y in range(1, stop + 1, 4):
            letter = temp_stacks[x][y]
            if letter.strip() != "":
                stacks[col] += letter
            col += 1

    # Parse moves
    new_moves = []
    for move in moves:
        move = move.replace("move", "").replace(" from", "").replace(" to", "")
        move = list(map(int, move.split()))

        count = move[0]
        fr = move[1] - 1
        to = move[2] - 1
        new_moves.append([count, fr, to])

    return (stacks, new_moves)


def solve1(stacks, moves):
    for move in moves:
        count, fr, to = move
        for i in range(count):
            # print(stacks)
            stacks[to] += stacks[fr][-1]
            stacks[fr] = stacks[fr][:-1]

    answer = ""
    for s in stacks:
        answer += s[-1]

    print("Part 1:", answer)
    return answer


def solve2(stacks, moves):
    # Parse moves Part 2
    for move in moves:
        count, fr, to = move
        start = len(stacks[fr]) - count
        end = len(stacks[fr])
        stacks[to] += stacks[fr][start:end]
        stacks[fr] = stacks[fr][:start]

    answer = ""
    for s in stacks:
        answer += s[-1]

    print("Part 2:", answer)
    return answer


def test(path):
    stacks, moves = parse_input(path + "sample.txt")
    stacks2 = stacks.copy()
    assert solve1(stacks, moves) == "CMZ"
    assert solve2(stacks2, moves) == "MCD"

    stacks, moves = parse_input(path + "input.txt")
    stacks2 = stacks.copy()
    assert solve1(stacks, moves) == "DHBJQJCCW"
    assert solve2(stacks2, moves) == "WJVRLSJJT"


if __name__ == "__main__":
    test("./")
