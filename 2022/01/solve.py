

def solve(filename):
    elves = []
    with open(filename, 'r') as handle:
        calories = 0
        for line in handle:        
            line = line.strip()
            try:            
                calories += int(line)
            except Exception as e:
                elves.append(calories)
                calories = 0
    elves.append(calories)

    # Part 1
    max_calories = max(elves)
    print("Part1:", max_calories)

    elves.sort(reverse=True)
    max_top_three = elves[0] + elves[1] + elves[2]
    print("Part2:", max_top_three)

    return (max_calories, max_top_three)


def test(path):
    part1, part2 = solve(path + "input.txt")
    assert part1 == 67658
    assert part2 == 200158


if __name__ == "__main__":
    test("./")