
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
    current_node = cup_map[current]
    picked = [current_node.next.data, current_node.next.next.data, current_node.next.next.next.data]
    # action 2: select destination
    destination_found = False
    destination = current - 1
    while not destination_found:
        if destination == 0:
            destination = max_cup_number
        if destination in picked:
            destination -= 1
        else:
            destination_found = True
    # print(f"current: {current}; picked: {picked}; dest: {destination}")
    # action 3: place picked cups to the right of the destination
    # -- move 1 --
    # cups: (3) 8  9  1  2  5  4  6  7 
    # pick up: 8, 9, 1
    # destination: 2
    dest_node = cup_map[destination]  # dest_node = 2
    temp = dest_node.next  # temp = 5
    dest_node.next = current_node.next  # set (2) point to (8)
    temp2 = current_node.next.next.next.next # temp2 = 2
    current_node.next.next.next.next = temp # set (1) point to (5)
    current_node.next = temp2 # set (3) => (2)
    # action 4: select new cup
    return current_node.next.data    


def solve_part1(puzzle_input, rounds):
    cups = [int(n) for n in puzzle_input]
    current = cups[0]

    cup_map = {}
    prev = None
    for c in cups:
        node = Node(c)
        cup_map[c] = node
        if prev is not None:
            prev.next = node
        prev = node    

    # complete the loop
    prev.next = cup_map[current]

    # temp = cup_map[current].next
    # while temp.data != current:
    #     print(f"{temp.data}->", end="")
    #     temp = temp.next    
    # exit()

    for _ in range(rounds):
        current = run_move(current, cup_map, 9)
        # print(f"CUPS: {cups}")
    
    # Starting after the cup labeled 1, collect the other cups' 
    # labels clockwise into a single string with no extra 
    # characters
    node = cup_map[1].next
    result = ''    
    while node.data != 1:
        result += str(node.data)
        node = node.next
    print(f"Result: {result}")
    return result


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# In the above example (389125467), this would be 934001 and then 159792; 
# multiplying these together produces 149245887792

# What if you created a linked list and then
# created a hashmap to map to those nodes??
# cups: { cup_num : node }
def solve_part2(puzzle_input, rounds):
    cups = [int(n) for n in puzzle_input]
    cups += list(range(10, 1000000 + 1))    

    current = cups[0]

    cup_map = {}
    prev = None
    for c in cups:
        node = Node(c)
        cup_map[c] = node
        if prev is not None:
            prev.next = node
        prev = node
    # complete the loop
    prev.next = cup_map[current]
    
    for _ in range(rounds):
        # print(f"round: {r}")
        current = run_move(current, cup_map, 1000000)
    result = cup_map[1].next.data * cup_map[1].next.next.data
    print(f"Result: {result}")
    return result

# Part 1
assert solve_part1('389125467', 10) == '92658374'
assert solve_part1('389125467', 100) == '67384529'
assert solve_part1('589174263', 100) == '43896725'

# Part 2
assert solve_part2('389125467', 10000000) == 149245887792
assert solve_part2('589174263', 10000000) == 2911418906