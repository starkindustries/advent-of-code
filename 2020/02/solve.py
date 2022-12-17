# Advent of Code 2020
# Day 2

filename = "input.txt"


def solve(filename, part2=False):
    validPasswords = 0
    with open(filename, "r") as handle:
        for line in handle:
            a, b, c = line.strip().split(" ")
            num1, num2 = map(int, a.split("-"))
            key = b[0]
            password = c

            if not part2:  # Part 1
                if num1 <= password.count(key) <= num2:
                    validPasswords += 1
            else:  # Part 2
                num1 -= 1
                num2 -= 1
                if password[num1] == key and password[num2] != key:
                    validPasswords += 1
                elif password[num1] != key and password[num2] == key:
                    validPasswords += 1
    part = 2 if part2 else 1
    print(f"Part {part}: {validPasswords}")
    return validPasswords


assert solve("input.txt") == 603
assert solve("input.txt", True) == 404
