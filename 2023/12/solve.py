import re
import functools

@functools.lru_cache(maxsize=None)
def is_valid_arrangement(springs, numbers):
    matches = re.findall("#+", springs)
    if len(numbers) != len(matches):
        return False
    for number, match in zip(numbers, matches):
        if number != len(match):
            return False
    return True

# Note for part2: decided to read a small hint found here:
# https://www.reddit.com/r/adventofcode/comments/18ghux0/comment/kd0npmi/?utm_source=share&utm_medium=web2x&context=3
# basically, if the first number matches the first '#' pattern in the springs then
# remove those items and recursive search that subset
@functools.lru_cache(maxsize=None)
def count_arrangements(springs, numbers):
    if springs and springs[0] == ".":
        return count_arrangements(springs[1:], numbers)
    if not springs and not numbers:
        return 1
    if not numbers:
        return 0 if "#" in springs else 1
    if not springs:
        return 0

    if springs[0] == "#":
        match = re.search("^#+", springs)
        assert match
        s_count = match.group().count("#")
        if s_count > numbers[0]:
            return 0
        if s_count == numbers[0]:
            # found matching pattern
            # return result of subset springs and numbers
            if s_count < len(springs) and springs[s_count] == "?":
                # if there is a '?' proceeding the hashes, it needs to be a dot '.'
                springs = springs[:s_count] + "." + springs[s_count+1:]
            return count_arrangements(springs[s_count+1:], numbers[1:])
        if s_count < numbers[0]:
            if s_count == len(springs):
                return 0
            if springs[s_count] == ".":
                return 0
            assert springs[s_count] == "?"
        # if none of the above conditions match, there is not enough info
        # continue to below

    try:
        q_index = springs.index("?")
    except ValueError:
        # no "?" in string
        # should not get to this case
        assert False

    s1 = springs[:q_index] + "#" + springs[q_index+1:]
    s2 = springs[:q_index] + "." + springs[q_index+1:]
    c1 = count_arrangements(s1, numbers)
    c2 = count_arrangements(s2, numbers)
    return c1 + c2


def solve(filename, part2=False):
    with open(filename, "r", encoding="utf8") as handle:
        lines = [line.strip() for line in handle.readlines()]

    ways = 0
    for line in lines:
        temp = line.split()
        springs = temp[0]
        numbers = tuple(map(int, temp[1].split(",")))
        
        if part2:
            springs = (springs + "?") * 4 + springs
            numbers = numbers * 5
        count = count_arrangements(springs, numbers)

        print(f"{springs} {numbers} ways:{count}")
        ways += count
        
    print(f"{ways=}")
    return ways

    

def test(path):
    assert count_arrangements("#?", (2,1)) == 0
    assert count_arrangements("", tuple()) == 1
    assert count_arrangements("..?..?..?", tuple()) == 1
    assert count_arrangements("#.?..?..?", (1,)) == 1
    assert count_arrangements("???.###", (1,1,3)) == 1
    assert count_arrangements(".??..??...?##.", (1,1,3)) == 4
    assert count_arrangements("?###????????", (3,2,1)) == 10

    assert solve(path + "sample.txt")  == 21
    assert solve(path + "sample.txt", True) == 525152

    assert solve(path + "input.txt") == 7460
    assert solve(path + "input.txt", True) == 6720660274964

if __name__ == "__main__":
    test("./")
