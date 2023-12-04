def solve(filename):
    total = 0
    with open(filename, "r", encoding="utf8") as handle:
        lines = handle.readlines()
    for line in lines:
        line = line.strip()
        line = line.replace("  ", " ")
        temp = line.split(":")
        cards = temp[1]
        temp = cards.split("|")
        winning = temp[0]
        owned = temp[1]
        print(winning, owned)
        winning = set(map(int,(winning.strip().split(" "))))
        owned = set(map(int, (owned.strip().split(" "))))
        print(winning, owned)

        points = 0
        for num in owned:
            if num in winning:
                if points == 0:
                    points = 1
                else:
                    points += points
        total += points
    print(total)
    return total

def solve2(filename):
    copies = {}
    with open(filename, "r", encoding="utf8") as handle:
        lines = handle.readlines()
    for line in lines:
        line = line.strip()
        line = line.replace("   ", " ")
        line = line.replace("  ", " ")
        temp = line.split(":")
        card_num = int(temp[0].strip().split(" ")[1].strip())
        print("CARD NUM", card_num)
        cards = temp[1]
        temp = cards.split("|")
        winning = temp[0]
        owned = temp[1]
        print(winning, owned)
        winning = set(map(int,(winning.strip().split(" "))))
        owned = set(map(int, (owned.strip().split(" "))))

        copies.setdefault(card_num, 0)
        copies[card_num] += 1

        multiplier = copies[card_num]
        card_num_copy = card_num
        matches = 0
        for num in owned:
            if num in winning:
                matches += 1
        for i in range(1, matches + 1):
            copies.setdefault(card_num + i, 0)
            copies[card_num + i] += 1 * copies[card_num]
    total = 0
    for card_num in copies:
        total += copies[card_num]
        
    print(total)
    return total

def test(path):
    part1 = solve(path + "sample.txt")
    assert part1 == 13
    part2 = solve2(path + "sample.txt")
    assert part2 == 30
    print("Test successful")

    solve(path + "input.txt")
    solve2(path + "input.txt")

if __name__ == "__main__":
    test("./")
