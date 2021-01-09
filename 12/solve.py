from math import cos, sin, pi

filename = "input.txt"
# filename = "sample.txt"

# Part 1 instructions parser


def processInstruction(i, x, y, r):
    action = i[0]
    value = int(i[1:])
    if action == "N":
        return x, y+value, r
    elif action == "S":
        return x, y-value, r
    elif action == "E":
        return x+value, y, r
    elif action == "W":
        return x-value, y, r
    elif action == "L":
        return x, y, (r-value) % 360
    elif action == "R":
        return x, y, (r+value) % 360
    elif action == "F":
        # North
        if r == 0:
            return x, y+value, r
        # East
        elif r == 90 or r == -270:
            return x+value, y, r
        # South
        elif r == 180 or r == -180:
            return x, y-value, r
        # WEst
        elif r == 270 or r == -90:
            return x-value, y, r
    print(f"Error at instruction: {i}. Position: {x},{y},{r}")

# Part 2 instructions parser


def processInstruction2(i, wx, wy, x, y):
    action = i[0]
    value = int(i[1:])
    if action == "N":
        return wx, wy+value, x, y
    elif action == "S":
        return wx, wy-value, x, y
    elif action == "E":
        return wx+value, wy, x, y
    elif action == "W":
        return wx-value, wy, x, y
    elif action in ["L", "R"]:
        if action == "R":
            value = -value
        # convert to radians
        value = value * (pi / 180)
        # Rotating a point about another point (2D)
        # https://stackoverflow.com/questions/2259476/rotating-a-point-about-another-point-2d
        # x' = x*cos(theta)-y*sin(theta)
        # y' = x*sin(theta)+y*cos(theta)
        wx2 = round(wx * cos(value) - wy * sin(value))
        wy2 = round(wx * sin(value) + wy * cos(value))
        return wx2, wy2, x, y
    elif action == "F":
        return wx, wy, (x+wx*value), (y+wy*value)
    print(f"Error at instruction: {i}. Position: {x},{y},{r}")


# Part 1
x, y, r = 0, 0, 90

# Part 2
# waypoint starts 10 units east and 1 unit north relative to the ship
# wx & wy are waypoint coordinates
# x2 & y2 are ship coordinates
wx, wy, x2, y2 = 10, 1, 0, 0

# Open file and process input
with open(filename, 'r') as handle:
    for line in handle:
        line = line.strip()
        x, y, r = processInstruction(line, x, y, r)
        wx, wy, x2, y2 = processInstruction2(line, wx, wy, x2, y2)
        # print(wx, " ", wy, " ", x2, " ", y2, " : ", line)
# Part 1
print(f"Position part 1: {x} + {y} = {abs(x) + abs(y)}")

# Part 2
print(f"Position part 2: {x2} + {y2} = {abs(x2) + abs(y2)}")
