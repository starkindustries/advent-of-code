
with open("input.txt") as file:
    lines = file.readlines()

# part 1

total = 0
for line in lines:
    line = line.strip()
    for my_char in line:
        if my_char.isdigit():
            first_number = my_char
            break
    for my_char in line[::-1]:
        if my_char.isdigit():
            second_number = my_char
            break
    str_number = first_number + second_number
    int_number = int(str_number)
    print(int_number)
    total += int_number
print(total)

# part 2

str_digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]



total = 0
for line in lines:
    numbers = []
    line = line.strip()
    for i in range(len(line)):
        my_char = line[i]
        if my_char.isdigit():
            numbers.append(my_char)
            continue
        for j, digit in enumerate(str_digits):
            # python's string slicing prevents IndexError so don't need to worry about going out of bounds
            my_digit = line[i:i+len(digit)]
            # print("mydigit ", my_digit, ":", digit, ":", line)
            if digit == my_digit:
                number = str(j + 1)
                numbers.append(number)
                break

    print("numbers", numbers)
    str_number = numbers[0] + numbers[-1]
    int_number = int(str_number)
    print(int_number)
    total += int_number
print("part2")
print(total)