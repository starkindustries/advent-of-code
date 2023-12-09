
def solve(filename, part2=False):
    with open(filename, "r", encoding="utf8") as handle:
        lines = handle.readlines()

    part1 = 0
    part2 = 0
    for line in lines:
        sequence = list(map(int, line.strip().split()))
        sequences = []
        sequences.append(sequence)
        while True:
            temp_seq = []
            for i in range(len(sequence) - 1):
                diff = sequence[i+1] - sequence[i]
                temp_seq.append(diff)
            sequences.append(temp_seq)
            is_all_zero = True
            for num in temp_seq:
                if num != 0:
                    is_all_zero = False
            if is_all_zero:
                break
            sequence = temp_seq
        next_value = 0
        previous_value = 0
        sequences.reverse()
        for seq in sequences:
            next_value = seq[-1] + next_value
            previous_value = seq[0] - previous_value
        print(next_value, previous_value)
        part1 += next_value
        part2 += previous_value

    return part1, part2

def test(path):
    assert solve(path + "sample.txt") == (114, 2)
    print("Test successful")

    result = solve(path + "input.txt")
    print("RESULT")
    print(result)

if __name__ == "__main__":
    test("./")
