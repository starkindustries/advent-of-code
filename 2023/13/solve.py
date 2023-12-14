def find_reflection(pattern, is_vert=False, prev_match=None):
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
                match = (y, y+1, int(is_vert))
                if prev_match and match != prev_match:
                    return match
                if not prev_match:
                    return match
    return None

def printmap(mymap, match, smudge, is_vert=False):
    header = "01234567890123456789"
    header = "    " + header[:len(mymap[0])]
    print(header)
    for y, row in enumerate(mymap):
        temp = "".join(row)
        if smudge[1] == y:
            x = smudge[0]
            mark = "H" if temp[x] == "#" else "*"
            temp = temp[:x] + mark + temp[x+1:]
        if not is_vert and y in match[:2]:
            temp += " <"
        temp = f"{str(y):>2}  " + temp
        print(temp)
    if is_vert:
        new_row = "    "
        for i in range(len(mymap[0])):
            if i in match[:2]:
                new_row += "^"
            else:
                new_row += " "
        print(new_row)

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
    
    # part1
    summary = 0
    matches = []
    for pattern in patterns:
        # search horizontal reflection
        match = find_reflection(pattern)
        if match:
            # add 1 to index because example is 1-based
            summary += (match[0] + 1) * 100
            print("found horizontal", match)
            matches.append(match) # for part2
            continue

        # search vertical reflection
        columns = [""] * len(pattern[0])
        for row in pattern:
            for x, col in enumerate(row):
                columns[x] += col
        
        match = find_reflection(columns, True)
        assert match
        matches.append(match) # for part2
        summary += match[0] + 1
    part1 = summary

    # part2
    assert len(matches) == len(patterns)
    summary = 0
    for index, pattern in enumerate(patterns):
        prev_match = matches[index]
        match_found = False
        for y in range(len(pattern)):
            for x in range(len(pattern[0])):
                new_pattern = pattern.copy()
                swap = "#" if pattern[y][x] == "." else "."
                new_pattern[y] = pattern[y][:x] + swap + pattern[y][x+1:]

                # search horizontal reflection
                match = find_reflection(new_pattern, False, prev_match)
                if match and match != prev_match:
                    match_found = True
                    # add 1 to index because example is 1-based
                    summary += (match[0] + 1) * 100
                    print(f"horizontal {match=} {prev_match=} smudge=({x},{y})")
                    printmap(new_pattern, match, (x, y))
                    break

                # search vertical reflection
                columns = [""] * len(pattern[0])
                for row in new_pattern:
                    for x, col in enumerate(row):
                        columns[x] += col
                
                match = find_reflection(columns, True, prev_match)
                if match and match != prev_match:
                    match_found = True
                    summary += match[0] + 1
                    print(f"vertical {match=} {prev_match=} smudge=({x},{y})")
                    printmap(new_pattern, match, (x, y), True)
                    break
            if match_found:
                break
        assert match_found
    part2=summary

    print(part1, part2)
    return part1, part2


def test(path):
    assert solve(path + "sample.txt")  == (405, 400)
    assert solve(path + "input.txt") == (30575, 37478)

if __name__ == "__main__":
    test("./")
