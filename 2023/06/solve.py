def solve(filename):
    with open(filename, "r", encoding="utf8") as handle:
        lines = handle.readlines()
    
    times = list(map(int, lines[0].split(":")[1].split()))
    distances = list(map(int, lines[1].split(":")[1].split()))
    
    wins = []
    for time, dist  in zip(times, distances):
        ways_to_win = 0
        for hold in range(1, time):
            d = hold * (time - hold)
            if d > dist:
                ways_to_win += 1
        wins.append(ways_to_win)
    
    part1 = 1
    for w in wins:
        part1 *= w

    # part2
    time2 = int(''.join(list(map(str, times))))
    dist2 = int(''.join(list(map(str, distances))))
    print(time2, dist2)
    ways_to_win = 0
    for hold in range(1, time2):
        d = hold * (time2 - hold)
        if d > dist2:
            ways_to_win += 1
    part2 = ways_to_win

    return part1, part2

def test(path):
    part1, part2 = solve(path + "sample.txt")
    print(part1, part2)
    assert part1 == 288
    assert part2 == 71503
    print("Test successful")

    res = solve(path + "input.txt")
    print(res)

if __name__ == "__main__":
    test("./")
