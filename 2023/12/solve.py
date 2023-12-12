import re

def is_valid_arrangement(springs, numbers):
    num_index = 0
    damaged = 0
    for i, s in enumerate(springs):
        if s == "#":
            damaged += 1
            if num_index >= len(numbers):
                return False
            if damaged > numbers[num_index]:
                return False
        if s in "." and i > 0 and springs[i-1] == "#":
            if damaged < numbers[num_index]:
                return False
            num_index += 1
            damaged = 0
    if springs[-1] == "#":
        # if springs ends with '#' then check final number
        if damaged < numbers[num_index]:
            return False
        num_index += 1

    if num_index < len(numbers):
        # in this case, we did not iterate through all number requirements
        return False
    # a quick sanity check
    # assert springs.count("#") == sum(numbers)
    # print("VALID", springs, numbers)
    return True

def count_arrangements(springs, numbers):
    try:
        q_index = springs.index("?")
    except ValueError:
        # no "?" in string
        if is_valid_arrangement(springs, numbers):
            return 1
        return 0
    
    # Prune step
    sub = springs[:q_index]
    last_hash_group = sub.rfind("#.")
    if last_hash_group != -1:
        sub = sub[:last_hash_group+1]
        matches = len(re.findall("#+", sub))
        if not sub or matches < 1:
            # Not enough data, do nothing
            pass
        elif not is_valid_arrangement(sub, numbers[:matches]):
            # print("CA:", springs, numbers, sub, numbers[:matches], q_index)
            return False

    s1 = springs[:q_index] + "#" + springs[q_index+1:]
    w1 = count_arrangements(s1, numbers)
    s2 = springs[:q_index] + "." + springs[q_index+1:]
    w2 = count_arrangements(s2, numbers)
    return w1 + w2

def solve(filename, part2=False):
    with open(filename, "r", encoding="utf8") as handle:
        lines = [line.strip() for line in handle.readlines()]

    ways = 0
    for line in lines:
        temp = line.split()
        springs = temp[0]
        numbers = list(map(int, temp[1].split(",")))
        if part2:
            springs = (springs + "?") * 4 + springs
            numbers = numbers * 5
        print(springs, numbers)
        count = count_arrangements(springs, numbers)
        print(f"{springs} {numbers} ways:{count}")
        ways += count
        
    print(ways)
    return ways

    

def test(path):
    test_data = """
        #.#.### 1,1,3
        .#...#....###. 1,1,3
        .#.###.#.###### 1,3,1,6
        ####.#...#... 4,1,1
        #....######..#####. 1,6,5
        .###.##....# 3,2,1
    """
    for item in test_data.split("\n"):
        temp = item.strip().split()
        if not temp:
            continue
        springs = temp[0]
        numbers = list(map(int, temp[1].split(",")))
        print(springs, numbers)
        assert is_valid_arrangement(springs, numbers)

    assert solve(path + "sample.txt")  == 21
    assert solve(path + "sample.txt", True) == 525152
    # assert solve(path + "sample.txt") == 8410
    # assert solve(path + "input.txt")  == 9312968 # part1
    # assert solve(path + "input.txt") == 597714117556 # part2
    # answer 10920 too high
    solve(path + "input.txt") == 7460
    solve(path + "input.txt", True)

if __name__ == "__main__":
    test("./")
