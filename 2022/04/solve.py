

# Part 1
def left_fully_contains_right(left, right):
    if left[0] <= right[0] and left[1] >= right[1]:
        return True
    return False

overlaps = 0
filename = "input.txt"


with open(filename, 'r') as handle:
    for line in handle:        
        pairs = [list(map(int, x.split("-"))) for x in line.strip().split(",")]
        print(pairs)
        if left_fully_contains_right(pairs[0], pairs[1]) or left_fully_contains_right(pairs[1], pairs[0]):
            overlaps += 1
print("Part 1:", overlaps)


# Part 2
def is_overlapping(left, right):
    if (right[0] <= left[0] <= right[1]) or (right[0] <= left[1] <= right[1]):
        return True
    return False


overlaps2 = 0
with open(filename, 'r') as handle:
    for line in handle:        
        pairs = [list(map(int, x.split("-"))) for x in line.strip().split(",")]
        print(pairs)
        if is_overlapping(pairs[0], pairs[1]) or is_overlapping(pairs[1], pairs[0]):
            overlaps2 += 1
print("Part 2:", overlaps2)