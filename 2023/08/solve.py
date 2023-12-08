import math

def solve(filename, part2=False):
    with open(filename, "r", encoding="utf8") as handle:
        lines = handle.readlines()
    
    instructions = lines.pop(0).strip()
    camelmap = {}
    paths = []

    for line in lines:
        line = line.strip()
        if line == "":
            continue
        data = line.split(" = ")
        element = data[0].strip()
        left, right = data[1].replace("(", "").replace(")", "").split(", ")
        camelmap[element] = (left, right)
        if element[-1] == "A":
            paths.append(element) # for part2
        # print(element, left, right, camelmap)

    if not part2:
        goal = "ZZZ"
        current = "AAA"
        steps = 0
        while current != goal:
            direction = instructions[steps % len(instructions)]
            if direction == "L":
                current = camelmap[current][0]
            elif direction == "R":
                current = camelmap[current][1]
            steps += 1
        result = steps

    if part2:
        steps_arr = []
        for i, path in enumerate(paths):
            steps = 0
            while True:
                if path[-1] == "Z":
                    steps_arr.append(steps)
                    break
                direction = instructions[steps % len(instructions)]
                dir_num = 0 if direction == "L" else 1
                path = camelmap[path][dir_num]
                steps += 1
        print(*steps_arr)
        result = math.lcm(*steps_arr)        
        print(result)

    return result

def test(path):
    part1 = solve(path + "sample.txt")
    print(part1)
    assert solve(path + "sample.txt") == 2
    assert solve(path + "sample2.txt") == 6
    assert solve(path + "sample3.txt", True) == 6
    # assert part2 == 5905
    print("Test successful")

    part1 = solve(path + "input.txt")
    # part2 = solve(path + "input.txt", True)
    print(part1)
    assert part1 == 12083
    part2 = solve(path + "input.txt", True)
    print(part2)
    assert part2 == 13385272668829
    # print(part1, part2)

if __name__ == "__main__":
    test("./")
