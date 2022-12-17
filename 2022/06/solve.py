from collections import deque


def find_marker(datastream, marker_length):
    last_matching_index = -1
    last4 = deque([])
    marker = 0
    for char in datastream:
        try:
            index = -1
            # match found at index
            # this index needs to get dropped off
            for i in range(len(last4) - 1, -1, -1):
                if last4[i] == char:
                    index = i
                    break
            if index > last_matching_index:
                last_matching_index = index
        except Exception as e:
            print(e, char)

        last4.append(char)
        # print("TEMP", last4)
        marker += 1
        if len(last4) > marker_length:
            last4.popleft()
            last_matching_index -= 1
        # print(char, last4, last_matching_index)
        if last_matching_index < 0 and marker >= marker_length:
            # Found start-of-packet marker
            break
    return marker


def solve(filename, marker_length):
    results = []
    with open(filename, "r", encoding="utf8") as handle:
        for line in handle:
            datastream = line.strip()
            result = find_marker(datastream, marker_length)
            results.append(result)
            print("Part 1 sample:", result)
    return results


def test(path):
    part1 = solve(path + "sample.txt", 4)
    part2 = solve(path + "sample.txt", 14)
    assert part1 == [7, 5, 6, 10, 11]
    assert part2 == [19, 23, 23, 29, 26]

    part1 = solve(path + "input.txt", 4)
    part2 = solve(path + "input.txt", 14)
    assert len(part1) == len(part2) == 1
    assert part1 == [1623]
    assert part2 == [3774]


if __name__ == "__main__":
    test("./")
