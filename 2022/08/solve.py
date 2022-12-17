def is_visible(row, col, map):
    tree = map[row][col]
    # check left
    i = col - 1
    visible = True
    while i >= 0:
        if map[row][i] >= tree:
            visible = False
            break
        i -= 1
    if visible:
        return True
    # check right
    i = col + 1
    visible = True
    while i < len(map[0]):
        if map[row][i] >= tree:
            visible = False
        i += 1
    if visible:
        return True
    # up
    i = row - 1
    visible = True
    while i >= 0:
        if map[i][col] >= tree:
            visible = False
        i -= 1
    if visible:
        return True
    # down
    i = row + 1
    visible = True
    while i < len(map):
        if map[i][col] >= tree:
            visible = False
        i += 1
    if visible:
        return True
    return False


def scenic_score(row, col, map):
    left = 0
    tree = map[row][col]
    # check left
    i = col - 1
    visible = True
    while i >= 0:
        left += 1
        if map[row][i] >= tree:
            break
        i -= 1
    # check right
    right = 0
    i = col + 1
    while i < len(map[0]):
        right += 1
        if map[row][i] >= tree:
            break
        i += 1
    # up
    up = 0
    i = row - 1
    while i >= 0:
        up += 1
        if map[i][col] >= tree:
            break
        i -= 1
    # down
    down = 0
    i = row + 1
    while i < len(map):
        down += 1
        if map[i][col] >= tree:
            break
        i += 1
    score = left * right * up * down
    # print(row, col, score)
    return score


def solve(filename):
    # Parse input
    trees = []
    with open(filename, "r") as handle:
        for line in handle:
            line = line.strip()
            tree_line = [int(x) for x in line]
            trees.append(tree_line)

    # Part 1
    num_visible = 0
    for row in range(1, len(trees) - 1, 1):
        for col in range(1, len(trees[0]) - 1, 1):
            if is_visible(row, col, trees):
                num_visible += 1
    num_visible += len(trees) * 2 + len(trees[0]) * 2 - 4
    print("Part 1:", num_visible)

    # Part 2
    scores = []
    for row in range(len(trees)):
        for col in range(len(trees[0])):
            score = scenic_score(row, col, trees)
            scores.append(score)
    print("Part 2:", max(scores))
    return num_visible, max(scores)


def test(path):
    part1, part2 = solve(path + "sample.txt")
    assert part1 == 21
    assert part2 == 8

    part1, part2 = solve(path + "input.txt")
    assert part1 == 1708
    assert part2 == 504000
