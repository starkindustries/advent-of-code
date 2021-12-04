# Sample [0, 3, 6]
# Turn 4: 0, [0, 3, 6, 0]
# Turn 5: 3, [0, 3, 6, 0, 3]


def solve(puzzle_input, target):
    spoken_record = {}
    for i, n in enumerate(puzzle_input):
        spoken_record.setdefault(n, []).append(i)
    last_spoken = puzzle_input[-1]
    turn = len(puzzle_input)

    while turn < target:
        if len(spoken_record[last_spoken]) == 1:
            # "Consider the last number spoken, 6. Since that was the first time the
            # number had been spoken, the 4th number spoken is 0."
            last_spoken = 0
            spoken_record.setdefault(0, []).append(turn)
        elif len(spoken_record[last_spoken]) > 1:
            # "Again consider the last number spoken, 0. Since it had been spoken before,
            # the next number to speak is the difference between the turn number when it
            # was last spoken (the previous turn, 4) and the turn number of the time it
            # was most recently spoken before then (turn 1)."
            last_spoken = spoken_record[last_spoken][-1] - \
                spoken_record[last_spoken][-2]
            spoken_record.setdefault(last_spoken, []).append(turn)
        elif last_spoken not in spoken_record:
            print(
                f"ERROR: last_spoken {last_spoken} not found in record: {spoken_record}")
        else:
            print("ERROR: unknown error occurred in solve() function")
        turn += 1
    return last_spoken


# ********************
# Part 1
# ********************
# Examples
assert solve([0, 3, 6], 2020) == 436
assert solve([1, 3, 2], 2020) == 1
assert solve([2, 1, 3], 2020) == 10
assert solve([1, 2, 3], 2020) == 27
assert solve([2, 3, 1], 2020) == 78
assert solve([3, 2, 1], 2020) == 438
assert solve([3, 1, 2], 2020) == 1836

# puzzle input
puzzle_input = [0, 14, 6, 20, 1, 4]
result = solve(puzzle_input, 2020)
print(f"Part 1: {result}")

# ********************
# Part 2
# ********************
# puzzle input
puzzle_input = [0, 14, 6, 20, 1, 4]
result = solve(puzzle_input, 30000000)
print(f"Part 1: {result}")
