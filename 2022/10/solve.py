

# 20th, 60th, 100th, 140th, 180th, and 220th
def solve():
    pass


x = 1
history = [1]
filename = "input.txt"
with open(filename, 'r') as handle:
    for line in handle:        
        if line.strip() == "noop":
            history.append(x)
        else:
            # addx
            instruction, number = line.strip().split()
            number = int(number)
            history.append(x)
            x += number
            history.append(x)

# for i, h in enumerate(history):
#     print(i, ":", h)

signal_strength = 0
signals = [20, 60, 100, 140, 180, 220]
for signal in signals:
    print(signal, history[signal-2])
    signal_strength += signal * history[signal-2]
print("Signal", signal_strength)

# Part 2

screen = [""]*6
crt_row = 0
crt_col = 0
cycle = 1
x = 1

for x in history:
    try:
        if abs(x - crt_col) <= 1:
            screen[crt_row] += "#"
        else:
            screen[crt_row] += "."
        crt_col += 1
        if crt_col == 40:
            crt_col = 0
            crt_row += 1
    except:
        continue
for line in screen:
    print(line)
# for index in history:
#     if 

# with open(filename, 'r') as handle:
#     for line in handle:

#         if abs(x - crt_col) <= 1:
#             screen[crt_row] += "#"
#         else:
#             screen[crt_row] += "."
        


#         if line.strip() == "noop":
#             continue
#         else:
#             # addx
#             instruction, number = line.strip().split()
#             number = int(number)            
#             x += number
