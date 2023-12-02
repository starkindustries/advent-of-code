
with open("input.txt") as file:
    lines = file.readlines()

# part 1

total = 0
max_red = 12
max_green = 13
max_blue = 14
for line in lines:
    line = line.strip()
    data = line.split(":")
    left = data[0]
    game_number = left.split(" ")[1]
    games = data[1].split(";")
    print(game_number, " : ", games)

    is_possible = True

    for sub_game in games:
        num_and_colors = sub_game.split(",")
        possible = True
        for num_color in num_and_colors:
            num_color = num_color.strip()
            num_color_data = num_color.split(" ")
            cube_num = int(num_color_data[0])
            color = num_color_data[1]
            print("DATA", cube_num, color)
            if color == "blue" and cube_num > max_blue:
                possible = False
                break
            if color == "red" and cube_num > max_red:
                possible = False
                break
            if color == "green" and cube_num > max_green:
                possible = False
                break
        if not possible:
            is_possible = False
            break
    if is_possible:
        print("possible: ", game_number)
        total += int(game_number)
print(total)

# part 2

total = 0
for line in lines:
    line = line.strip()
    data = line.split(":")
    left = data[0]
    game_number = left.split(" ")[1]
    games = data[1].split(";")
    print(game_number, " : ", games)

    min_red = 0
    min_blue = 0
    min_green = 0

    for sub_game in games:
        num_and_colors = sub_game.split(",")
        possible = True
        for num_color in num_and_colors:
            num_color = num_color.strip()
            num_color_data = num_color.split(" ")
            cube_num = int(num_color_data[0])
            color = num_color_data[1]
            print("DATA", cube_num, color)
            if color == "blue" and cube_num > min_blue:
                min_blue = cube_num
            elif color == "red" and cube_num > min_red:
                min_red = cube_num
            elif color == "green" and cube_num > min_green:
                min_green = cube_num
    power = min_red * min_green * min_blue
    print("POWER: ", power)
    total += power

print(total)