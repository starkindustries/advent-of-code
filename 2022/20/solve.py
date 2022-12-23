
from collections import deque


# i num
# 0   1
# 1   2
# 2  -3
# 3   3
# 4  -2
# 5   0
# 6   4


def find_number_at(original_index, numbers):
    for index, number in enumerate(numbers):
        if number[1] == original_index:
            return number[0], index


numbers = deque()
multiplyer = 811589153

filename = "input.txt"
with open(filename, "r") as handle:
    for index, line in enumerate(handle):
        line = int(line.strip())
        numbers.append((line * multiplyer, index))

sample=[
    [1, 2, -3, 3, -2, 0, 4],
    [2, 1, -3, 3, -2, 0, 4],
    [1, -3, 2, 3, -2, 0, 4],
    [1, 2, 3, -2, -3, 0, 4],
    [1, 2, -2, -3, 0, 3, 4],
    [1, 2, -3, 0, 3, 4, -2],
    [1, 2, -3, 0, 3, 4, -2],
    [1, 2, -3, 4, 0, 3, -2]
]

# print(numbers)
# print([x[0] for x in numbers])
# print(sample.pop(0))


NUM_ELEMENTS = len(numbers)
rounds = 10
for _ in range(rounds):
    for original_index in range(NUM_ELEMENTS):
        number, index = find_number_at(original_index, numbers)
        # number, times_placed = numbers[index]    
        # if times_placed == round + 1:
        #     index += 1
        #     continue
        # else:
        del numbers[index]
        new_index = (index + number) % len(numbers)
        # the number gets deleted from the array
        # all numbers after and including index get shifted to the left by one
        # therefore, adjust the new_index by -1 if new_index is
        # greater than current index
        # every number a
        # if new_index < index:
        #     new_index += 1
        # if number < 0:
        #     new_index = (index + number - 1) % len(numbers)        
        # if new_index <= len(numbers):
        #     new_index %= len(numbers)
        # if new_index < 0 and -new_index > len(numbers):
        #     new_index %= len(numbers)                
        
        # print()
        # print([x[0] for x in numbers])
        numbers.insert(new_index, (number, original_index))
        # temp1 = [x[0] for x in numbers]
        # temp2 = sample.pop(0)
        # equals = (temp1 == temp2)
        # print(f"yours:  {temp1}, num {number}, index: {index}, new index {new_index}")
        # print(f"sample: {temp2}, {equals}")
        # input()

# for item in numbers:
#     num, is_placed = item
#     if not is_placed:
#         print(item, "NOT PLACED")
#         input()
print(numbers)
print("LEN NUM:", len(numbers))
zero_index = [index for index, x in enumerate(numbers) if x[0] == 0][0]
print("zero", zero_index)
grove_coords_sum = 0
coords = [1000, 2000, 3000]
for coord in coords:
    index = (coord + zero_index) % len(numbers)
    print(coord, index, numbers[index])
    grove_coords_sum += numbers[index][0]

# grove_coords_sum2 = 0
# for coord in coords:
#     for i in range(1, coord + 1, 1):
#         index = i + zero_index
#         if index >= len(numbers):
#             index 
#     print(coord, index, numbers[index])
#     grove_coords_sum2 += numbers[index][0]

print("part1", grove_coords_sum)
print("part2", grove_coords_sum, "sample", 1623178306)

if rounds == 1 and filename == "sample.txt":
    assert grove_coords_sum == 3
if rounds == 10 and filename == "sample.txt":
    assert grove_coords_sum == 1623178306
if rounds == 1 and filename == "input.txt":
    assert grove_coords_sum == 18257
if rounds == 10 and filename == "input.txt":
    assert grove_coords_sum == 4148032160983
# print("part1", grove_coords_sum2)

# wrong: -5555, -9746
# correct: 18257