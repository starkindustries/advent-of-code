# ****************
# Crab Actions
# ****************
# 1) The crab picks up the three cups that are immediately
# clockwise of the current cup. They are removed from
# the circle; cup spacing is adjusted as necessary to
# maintain the circle.

# 2) The crab selects a destination cup: the cup with a label
# equal to the current cup's label minus one. If this would
# select one of the cups that was just picked up, the crab
# will keep subtracting one until it finds a cup that
# wasn't just picked up. If at any point in this process
# the value goes below the lowest value on any cup's label,
# it wraps around to the highest value on any cup's label
# instead.

# 3) The crab places the cups it just picked up so that they are
# immediately clockwise of the destination cup. They keep the
# same order as when they were picked up.

# 4) The crab selects a new current cup: the cup which is
# immediately clockwise of the current cup.


def run_move(current, cup_map, max_cup_number):
    # action 1: pick up three cups
    picked = [current.next.data, current.next.next.data, current.next.next.next.data]

    # action 2: select destination
    dest_found = False
    dest_label = current.data - 1
    while not dest_found:
        if dest_label == 0:
            dest_label = max_cup_number
        if dest_label in picked:
            dest_label -= 1
        else:
            dest_found = True
    dest = cup_map[dest_label]

    # action 3: place picked cups to the right of the destination
    # ***********************
    # Move 1 from example:
    # ***********************
    # pick up: 8, 9, 1
    # destination: 2 ----.
    # cups: (3) 8  9  1  2  5  4  6  7
    # 1.     |        |  ^ dest (2) needs to point to first node picked (8)
    # 2.     |        ^ third picked (1) needs to point to dest's next node (5)
    # 3.     ^ current (3) needs to point to third picked's next node (2)
    temp1 = dest.next  # save dest's next (5)
    temp2 = current.next.next.next.next  # save third's next (2)
    dest.next = current.next  # reference 1 above
    current.next.next.next.next = temp1  # reference 2 above
    current.next = temp2  # reference 3 above

    # action 4: select new cup
    return current.next


def solve(puzzle_input, rounds, part2=False):
    cups = [int(n) for n in puzzle_input]
    if part2:
        cups += list(range(10, 1000000 + 1))

    cup_map = {}
    prev = None
    for c in cups:
        node = Node(c)
        cup_map[c] = node
        if prev is not None:
            prev.next = node
        prev = node

    # complete the loop
    prev.next = cup_map[cups[0]]

    # Compute the Rounds
    current = cup_map[cups[0]]
    max_cup = 9 if not part2 else 1000000
    for _ in range(rounds):
        current = run_move(current, cup_map, max_cup)

    # Part 1
    # "Starting after the cup labeled 1, collect the other cups'
    # labels clockwise into a single string with no extra
    # characters"
    if not part2:
        node = cup_map[1].next
        result = ""
        while node.data != 1:
            result += str(node.data)
            node = node.next
        print(f"Part 1: {result}")
        return result

    # Part 2
    # "In the above example (389125467), this would be 934001 and then 159792;
    # multiplying these together produces 149245887792"
    result = cup_map[1].next.data * cup_map[1].next.next.data
    print(f"Part 2: {result}")
    return result


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# Part 1
assert solve("389125467", 10) == "92658374"
assert solve("389125467", 100) == "67384529"
assert solve("589174263", 100) == "43896725"

# Part 2
assert solve("389125467", 10000000, True) == 149245887792
assert solve("589174263", 10000000, True) == 2911418906
