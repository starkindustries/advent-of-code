def find_reflection(pattern):
    for y in range(len(pattern)-1):
        row = pattern[y]
        next = pattern[y+1]
        if row == next:
            found_match = True
            left = y - 1
            right = y + 2
            while left >= 0 and right < len(pattern):
                if pattern[left] != pattern[right]:
                    found_match = False
                    break
                left += -1
                right += 1
            if found_match:
                print(f"match:", y, y+1)
                return (y, y+1)
    return None


def solve(filename, part2=False):
    with open(filename, "r", encoding="utf8") as handle:
        lines = [line.strip() for line in handle.readlines()]

    patterns = []
    pattern = []
    for line in lines:
        if not line:
            patterns.append(pattern)
            pattern = []
            continue
        pattern.append(line)

    if pattern:
        patterns.append(pattern)
    
    summary = 0
    for pattern in patterns:

        # search horizontal reflection
        match = find_reflection(pattern)
        if match:
            # add 1 to index because example is 1-based
            summary += (match[0] + 1) * 100
            print("found horizontal", match)
            continue

        # search vertical reflection
        columns = [""] * len(pattern[0])
        for row in pattern:
            for x, col in enumerate(row):
                columns[x] += col
        
        match = find_reflection(columns)
        assert match
        summary += match[0] + 1

    print(patterns)

    part1=summary
    print(part1)
    return part1


def test(path):
    assert solve(path + "sample.txt")  == 405
    # assert solve(path + "sample.txt", True) == 525152

    assert solve(path + "input.txt") == 30575
    # assert solve(path + "input.txt", True) == 6720660274964

if __name__ == "__main__":
    test("./")
