#
# Sample monkey data:
# monkey {
#     "items" : [79, 98],
#     "operation" : [ "*", 19 ],
#     "test" : 23,
#     "true" : 2,
#     "false" : 3
#     "count" = 0
# }
#
def simulate_monkey(index, monkeys, rounds, lcm):
    monkey = monkeys[index]
    while len(monkey["items"]) > 0:
        # Monkey inspects item
        item = monkey["items"].pop(0)
        monkey["count"] += 1

        # worry/item level is added/multiplied by [var]
        if monkey["operation"][0] == "*":
            if monkey["operation"][1] == "old":
                item *= item
            else:
                item *= int(monkey["operation"][1])
        elif monkey["operation"][0] == "+":
            if monkey["operation"][1] == "old":
                item += item
            else:
                item += int(monkey["operation"][1])

        # Monkey gets bored with item. Worry level is divided by 3
        if rounds == 20:
            # part 1 requires 20 sounds and worry // 3
            item = item // 3

        # modulo optimization
        modulo = monkey["test"]
        test_result = item % modulo
        if item > lcm:
            remainder = item % lcm
            item = lcm + remainder

        # divisibility test results. throw item to next monkey
        if test_result == 0:
            index = monkey["true"]
        else:
            index = monkey["false"]
        monkeys[index]["items"].append(item)


def solve(filename, rounds):
    monkeys = []
    with open(filename, "r", encoding="utf8") as handle:
        while True:
            # monkey index
            line = handle.readline()
            if line == "":
                break
            index = int(line.split()[1][:-1])
            monkeys.append({"count": 0})
            # starting items
            line = handle.readline()
            numbers = line.split(":")[1]
            numbers = list(map(int, numbers.split(",")))
            monkeys[index]["items"] = numbers
            # operation
            line = handle.readline()
            line = line.split("=")[1].split()
            monkeys[index]["operation"] = [line[1], line[2]]
            # test
            line = handle.readline()
            monkeys[index]["test"] = int(line.split("by")[1])
            # true
            line = handle.readline()
            monkeys[index]["true"] = int(line.split("monkey")[1])
            # false
            line = handle.readline()
            monkeys[index]["false"] = int(line.split("monkey")[1])
            # read in blank line
            line = handle.readline().strip()
            assert line == ""

    # least common multiple
    lcm = 1
    for monkey in monkeys:
        lcm *= monkey["test"]

    # monkey business
    for _ in range(rounds):
        for index in range(len(monkeys)):
            simulate_monkey(index, monkeys, rounds, lcm)

    # gather up inspection counts and multiply top two
    inspection_count = []
    for monkey in monkeys:
        inspection_count.append(monkey["count"])

    inspection_count.sort()
    answer = inspection_count.pop() * inspection_count.pop()
    print("part1", answer)
    return answer


def test(path):
    filename = path + "sample.txt"
    assert solve(filename, 20) == 10605
    assert solve(filename, 10000) == 2713310158

    filename = path + "input.txt"
    assert solve(filename, 20) == 107822
    assert solve(filename, 10000) == 27267163742


if __name__ == "__main__":
    test("./")
