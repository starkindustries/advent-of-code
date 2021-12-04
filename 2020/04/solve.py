# *************************
# part 1
# *************************
def passportIsValid(data):
    checksum = [0] * 7
    for line in data:
        # hgt:59cm byr:2029 cid:219 pid:9381688753 eyr:1992 hcl:#b6652a
        for item in line.split(" "):
            # hgt:59cm
            key, _ = item.split(":")
            if key == "byr":
                checksum[0] = 1
            elif key == "iyr":
                checksum[1] = 1
            elif key == "eyr":
                checksum[2] = 1
            elif key == "hgt":
                checksum[3] = 1
            elif key == "hcl":
                checksum[4] = 1
            elif key == "ecl":
                checksum[5] = 1
            elif key == "pid":
                checksum[6] = 1
    result = "".join(map(str, checksum))
    print(f"Result: {result}")
    if result == "1111111":
        return True
    return False


valid = 0
with open("input.txt", 'r') as handle:
    passportData = []
    for line in handle:
        line = line.strip()
        if line == "":
            if passportIsValid(passportData):
                valid += 1
            passportData = []
        else:
            passportData.append(line)
    if passportIsValid(passportData):
        valid += 1

print(f"Valid passports part 1: {valid}\n\n")

# *************************
# part 2
# *************************


def passportIsValid2(data):
    checksum = [0] * 7
    for line in data:
        for item in line.split(" "):
            key, value = item.split(":")
            # birth year
            if key == "byr":
                if not (1920 <= int(value) <= 2002):
                    print(f"invalid birth year: {value}")
                    return False
                checksum[0] = 1
            # issue year
            elif key == "iyr":
                if not (2010 <= int(value) <= 2020):
                    print(f"invalid issue year: {value}")
                    return False
                checksum[1] = 1
            # expiration
            elif key == "eyr":
                if not (2020 <= int(value) <= 2030):
                    print(f"invalid expiration year: {value}")
                    return False
                checksum[2] = 1
            # height
            elif key == "hgt":
                metric = value[-2:]
                height = 0
                try:
                    height = int(value[:-2])
                except:
                    print(f"invalid height conversion: {value}")
                    return False
                if metric not in ["cm", "in"]:
                    print(f"invalid metric: {value}")
                    return False
                if metric == "in":
                    if not (59 <= height <= 76):
                        print(f"invalid height (in): {value}")
                        return False
                elif metric == "cm":
                    if not (150 <= height <= 193):
                        print(f"invalid height (cm): {value}")
                        return False
                checksum[3] = 1
            # hair
            elif key == "hcl":
                if value[0] != "#":
                    print(f"invalid hair color, no hash#: {value}")
                    return False
                if len(value[1:]) != 6:
                    print(f"invalid hair color: {value}")
                    return False
                for char in value[1:]:
                    if char not in "0123456789abcdef":
                        print(f"invalid hair color: {value}")
                        return False
                checksum[4] = 1
            # eyes
            elif key == "ecl":
                if value not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
                    print(f"invalid eye color: {value}")
                    return False
                checksum[5] = 1
            # passport ID
            elif key == "pid":
                if len(value) != 9:
                    print(f"invalid passport id: {value}")
                    return False
                for digit in value:
                    try:
                        int(digit)
                    except:
                        print(f"invalid passport: {value}")
                        return False
                checksum[6] = 1
    result = "".join(map(str, checksum))
    # print(f"Result: {result}")
    if result == "1111111":
        return True
    return False


valid = 0
with open("input.txt", 'r') as handle:
    passportData = []
    for line in handle:
        line = line.strip()
        # print(f"line: {line}")
        if line == "":
            if passportIsValid2(passportData):
                # print(f"Valid passport: {passportData}")
                valid += 1
            # else:
                # print(f"INVALID passport: {passportData}")
            passportData = []
        else:
            passportData.append(line)
    if passportIsValid2(passportData):
        valid += 1

print(f"Valid passports part 2: {valid}")
