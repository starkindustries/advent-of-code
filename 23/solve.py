
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
def run_move(current_index, cups, max_cup_number):
    # action 1: pick up three cups
    current = cups[current_index]
    picked = []
    for _ in range(3):
        if current_index + 1 < len(cups):
            picked.append(cups.pop(current_index + 1))
        else:
            picked.append(cups.pop(0))    
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
    # print(f"current: {current}; picked: {picked}; cups: {cups}; dest: {destination}")
    # action 3: place picked cups to the right of the destination
    dest_index = cups.index(destination)
    for i, c in enumerate(picked):
        cups.insert(dest_index + i + 1, c)        
    # action 4: select new cup
    if dest_index < current_index:
        current_index += 3
    if current_index + 1 < len(cups):
        return current_index + 1
    return 0  # current_index = 0


def solve_part1(puzzle_input, rounds):
    cups = [int(n) for n in puzzle_input]
    current_index = 0
    for _ in range(rounds):
        current_index = run_move(current_index, cups, 9)
        # print(f"CUPS: {cups}")
    
    # Starting after the cup labeled 1, collect the other cups' 
    # labels clockwise into a single string with no extra 
    # characters
    i = cups.index(1)
    result = cups[i+1:] + cups[:i]
    result = ''.join([str(n) for n in result])
    print(f"Result: {result}")
    return result

# In the above example (389125467), this would be 934001 and then 159792; 
# multiplying these together produces 149245887792
def solve_part2(puzzle_input, rounds):
    cups = [int(n) for n in puzzle_input]
    cups += list(range(10, 1000000 + 1))

    current_index = 0
    for r in range(rounds):
        print(f"round: {r}")
        current_index = run_move(current_index, cups, 1000000)
    i = cups.index(1)
    return cups[i+1] * cups[i+2]

# Part 1
assert solve_part1('389125467', 10) == '92658374'
assert solve_part1('389125467', 100) == '67384529'
assert solve_part1('589174263', 100) == '43896725'

# Part 2
assert solve_part2('389125467', 100000) == 149245887792