import functools

VALUES = {"A" : 14, "K" : 13, "Q" : 12, "J": 11, "T": 10}
for i in range(2, 10):
    VALUES[str(i)] = i
print(VALUES)

is_part2 = False

def compare(item1, item2):
    hand1, hand2 = item1[0], item2[0]
    assert len(hand1) == len(hand2) == 5
    for c1, c2 in zip(hand1, hand2):
        assert c1 in VALUES and c2 in VALUES
        if is_part2:
            VALUES["J"] = 1
        if VALUES[c1] < VALUES[c2]:
            return -1
        elif VALUES[c1] > VALUES[c2]:
            return 1
    return 0

def get_hand_type(handmap):
    has_three = False
    has_two = 0
    for _, count in handmap.items():
        if count == 5:
            return 6            
        if count == 4:
            return 5
        if count == 3:
            has_three = True
        if count == 2:
            has_two += 1
    if has_three and has_two == 1:
        return 4
    elif has_three:
        return 3
    elif has_two == 2: # two pair
        return 2
    elif has_two == 1:
        return 1
    else:
        return 0

def solve(filename, part2=False):
    global is_part2 
    is_part2 = True
    with open(filename, "r", encoding="utf8") as handle:
        lines = handle.readlines()
    
    hands = []
    for _ in range(7):
        hands.append([])
    for line in lines:
        line = line.strip()
        hand, bid = line.split()
        bid = int(bid)
        handmap = {}
        for char in hand:
            handmap.setdefault(char, 0)
            handmap[char] += 1
        
        if not part2:
            pass
        elif "J" not in handmap:
            pass
        elif handmap["J"] == 5:
            pass
        else:
            wilds = handmap["J"]
            # get largest pairing
            max_count = 0
            max_char = ""
            for char, count in handmap.items():
                if char == "J":
                    continue
                if count > max_count:
                    max_count = count
                    max_char = char
            print("max char", max_char, handmap)
            handmap[max_char] += wilds
            del handmap["J"] # don't need J in the map anymore

        # print(hand, bid, handmap)
        type = get_hand_type(handmap)
        hands[type].append((hand,bid))

    # all the hands are sorted by type
    # now sort by strength
    total = 0
    num_hands = len(lines)
    rank = 1
    for h in hands:
        temp = sorted(h, key=functools.cmp_to_key(compare))
        print(temp)
        for t in temp:
            bid = t[1]
            total += rank * bid
            rank += 1
    print(total)
    return total

def test(path):
    part1 = solve(path + "sample.txt")
    part2 = solve(path + "sample.txt", True)
    print(part1, part2)
    assert part1 == 6440
    assert part2 == 5905
    print("Test successful")

    part1 = solve(path + "input.txt")
    part2 = solve(path + "input.txt", True)
    print(part1, part2)

if __name__ == "__main__":
    test("./")
