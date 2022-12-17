def solve(filename):
    # Part 1
    def left_fully_contains_right(left, right):
        if left[0] <= right[0] and left[1] >= right[1]:
            return True
        return False

    overlaps = 0
    with open(filename, "r") as handle:
        for line in handle:
            pairs = [list(map(int, x.split("-"))) for x in line.strip().split(",")]
            print(pairs)
            if left_fully_contains_right(
                pairs[0], pairs[1]
            ) or left_fully_contains_right(pairs[1], pairs[0]):
                overlaps += 1
    print("Part 1:", overlaps)

    # Part 2
    def is_overlapping(left, right):
        if (right[0] <= left[0] <= right[1]) or (right[0] <= left[1] <= right[1]):
            return True
        return False

    overlaps2 = 0
    with open(filename, "r") as handle:
        for line in handle:
            pairs = [list(map(int, x.split("-"))) for x in line.strip().split(",")]
            print(pairs)
            if is_overlapping(pairs[0], pairs[1]) or is_overlapping(pairs[1], pairs[0]):
                overlaps2 += 1
    print("Part 2:", overlaps2)
    return overlaps, overlaps2


def test(path):
    part1, part2 = solve(path + "sample.txt")
    assert part1 == 2
    assert part2 == 4

    part1, part2 = solve(path + "input.txt")
    assert part1 == 599
    assert part2 == 928


if __name__ == "__main__":
    test("./")
