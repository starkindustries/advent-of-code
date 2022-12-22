
from collections import deque


# i num
# 0   1
# 1   2
# 2  -3
# 3   3
# 4  -2
# 5   0
# 6   4


numbers = deque()
filename = "input.txt"
with open(filename, "r") as handle:
    for line in handle:
        line = int(line.strip())
        numbers.append((line, False))

# print(numbers)
# print([x[0] for x in numbers])
index = 0
while index < len(numbers):
    number, is_placed = numbers[index]    
    if is_placed:
        index += 1    
        continue
    if number == 0:
        numbers[index] = (number, True)
        continue
    new_index = index + number
    if new_index >= len(numbers):
        new_index = new_index % len(numbers) + 1
    if new_index < 0 and -new_index > len(numbers):
        new_index %= len(numbers)
    del numbers[index]
    numbers.insert(new_index, (number, True))
    # print([x[0] for x in numbers])
    # input()

# for item in numbers:
#     num, is_placed = item
#     if not is_placed:
#         print(item, "NOT PLACED")
#         input()
print(numbers)
print("LEN NUM:", len(numbers))
zero_index = numbers.index((0, True))
print("zero", zero_index)
grove_coords_sum = 0
coords = [1000, 2000, 3000]
for coord in coords:
    index = (coord + zero_index) % len(numbers)
    print(coord, index, numbers[index])
    grove_coords_sum += numbers[index][0]

print("part1", grove_coords_sum)
