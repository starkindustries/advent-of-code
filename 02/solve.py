# Advent of Code 2020
# Day 2

filename = "input.txt"


def passwordIsValid(min, max, key, password):
    count = 0
    for letter in password:
        if key == letter:
            count += 1
    if min <= count <= max:
        return True
    return False


# part 1
# 13-14 f: ffffffffnfffvv
validPasswords = 0
with open(filename, 'r') as handle:
    for line in handle:
        a, b, c = line.strip().split(" ")
        min, max = map(int, a.split("-"))
        key = b[0]
        password = c

        print(f"{min}, {max}, {key}, {password}")
        if passwordIsValid(min, max, key, password):
            validPasswords += 1
print(f"Valid passwords part 1: {validPasswords}")

# part 2
validPasswords = 0
with open(filename, 'r') as handle:
    for line in handle:
        a, b, c = line.strip().split(" ")
        p1, p2 = map(int, a.split("-"))
        key = b[0]
        password = c

        print(f"{min}, {max}, {key}, {password}")
        p1 -= 1
        p2 -= 1
        if password[p1] == key and password[p2] != key:
            validPasswords += 1
        elif password[p1] != key and password[p2] == key:
            validPasswords += 1
print(f"Valid passwords part 2: {validPasswords}")
