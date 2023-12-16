def calculate_hash(string):
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256
    return value

def solve(filename, part2=False):
    with open(filename, "r", encoding="utf8") as handle:
        lines = [line.strip() for line in handle.readlines()]

    assert len(lines) == 1
    sequence = lines[0].split(",")
    
    # part1
    total = 0
    for item in sequence:
        total += calculate_hash(item)

    # part2
    boxes = {}
    for item in sequence:
        if "=" in item:
            temp = item.split("=")
            assert len(temp) == 2
            label, focal = temp[0], int(temp[1])
            box = calculate_hash(label)
            boxes.setdefault(box, [])
            lenses = boxes[box]
            replaced_lense = False
            for i, lense in enumerate(lenses):
                if label == lense[0]:
                    lenses[i] = (label, focal)
                    replaced_lense = True
                    break
            if not replaced_lense:
                boxes[box].append((label, focal))
        elif "-" in item:
            label = item[:-1]
            box = calculate_hash(label)
            boxes.setdefault(box, [])
            lenses = boxes[box]
            for i, lense in enumerate(lenses):
                if label == lense[0]:
                    lenses.pop(i)
                    break
        # print(item, label, " --- ", boxes)
        # input()
    
    focus_power = 0
    for box, lenses in boxes.items():
        for i, lense in enumerate(lenses):
            temp = (1+box) * (i+1) * lense[1]
            print(f"1+{box} * {i + 1} * {lense[1]} {lense[0]} = {temp}")
            focus_power += temp

    part1, part2 = total, focus_power
    print(part1, part2)
    return part1, part2


def test(path):
    assert calculate_hash("HASH") == 52
    assert calculate_hash("rn=1") == 30
    assert calculate_hash("cm-") == 253
    assert calculate_hash("rn") == 0
    assert calculate_hash("qp") == 1

    assert solve(path + "sample.txt") == (1320, 145)
    assert solve(path + "input.txt") == (518107, 303404)

if __name__ == "__main__":
    test("./")
