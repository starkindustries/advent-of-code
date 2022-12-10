

def solve(filename):
    x = 1
    history = []
    with open(filename, 'r', encoding="utf8") as handle:
        for line in handle:
            if line.strip() == "noop":
                history.append(x)
            else:
                # addx
                _, number = line.strip().split()
                number = int(number)
                history.extend([x, x])
                x += number

    # 20th, 60th, 100th, 140th, 180th, and 220th
    signals = [20, 60, 100, 140, 180, 220]
    total_strength = 0
    for signal in signals:
        strength = signal * history[signal-1]
        print(signal, history[signal-1], strength)
        total_strength += strength
    print("Signal strength:", total_strength)
    print()

    # Part 2

    screen = []
    screen_row = ""
    crt_col = 0

    for x in history:
        if abs(x - crt_col) <= 1:
            screen_row += "#"
        else:
            screen_row += "."
        crt_col += 1
        if crt_col == 40:
            crt_col = 0
            screen.append(screen_row)
            screen_row = ""

    for line in screen:
        print(line)
    return (total_strength, screen)


def is_matching(screen1, screen2):
    assert len(screen1) == len(screen2)
    for row1, row2 in zip(screen1, screen2):
        assert row1 == row2
    return True


def test(path):
    part2_sample = ["##..##..##..##..##..##..##..##..##..##..",
                    "###...###...###...###...###...###...###.",
                    "####....####....####....####....####....",
                    "#####.....#####.....#####.....#####.....",
                    "######......######......######......####",
                    "#######.......#######.......#######....."]

    part1, part2 = solve(path + "sample.txt")
    assert part1 == 13140
    assert is_matching(part2, part2_sample)

    part2_input = ["####.#..#.###..####.###....##..##..#....",
                   "#....#..#.#..#....#.#..#....#.#..#.#....",
                   "###..####.#..#...#..#..#....#.#....#....",
                   "#....#..#.###...#...###.....#.#.##.#....",
                   "#....#..#.#....#....#....#..#.#..#.#....",
                   "####.#..#.#....####.#.....##...###.####."]

    part1, part2 = solve(path + "input.txt")
    assert part1 == 12520
    assert is_matching(part2, part2_input)


if __name__ == "__main__":
    test("./")
