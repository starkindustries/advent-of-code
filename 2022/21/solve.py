import sys


monkeys = {} # { name : number or operation}

filename = "input.txt"
with open(filename, "r") as handle:
    for line in handle:
        line = line.strip().split()
        # print(line)
        if len(line) == 4:
            name = line[0][:-1]
            m1 = line[1]
            operation = line[2]
            m2 = line[3]
            monkeys[name] = (m1, operation, m2)
        elif len(line) == 2:
            name = line[0][:-1]
            number = int(line[1])
            monkeys[name] = number
        else:
            assert False


for name, values in monkeys.items():
    print(f"{name}, {values}")

def find_root(name, monkeys):
    value = monkeys[name]
    if isinstance(value, int):
        return value
    if isinstance(value, tuple):
        m1, op, m2 = value
        if op == "+":
            return find_root(m1, monkeys) + find_root(m2, monkeys)
        elif op == "-":
            return find_root(m1, monkeys) - find_root(m2, monkeys)
        elif op == "*":
            return find_root(m1, monkeys) * find_root(m2, monkeys)
        elif op == "/":
            return find_root(m1, monkeys) / find_root(m2, monkeys)


def find_root2(name, monkeys):
    value = monkeys[name]
    if name == "root":
        m1, op, m2 = value
        result1 = find_root2(m1, monkeys)
        result2 = find_root2(m2, monkeys)
        return (result1, "=", result2)
    elif name == "humn":
        return "x"
    elif isinstance(value, int):
        return value
    if isinstance(value, tuple):
        m1, op, m2 = value
        result1 = find_root2(m1, monkeys)
        result2 = find_root2(m2, monkeys)
        return (result1, op, result2)        


# def calculate(equation):
#     m1, op, m2 = equation
#     if isinstance(m1, int):
#         result1 = m1
#     elif isinstance(m1, tuple):
#         result1 = calculate(m1)
    
#     if isinstance(m2, int):
#         result2 = m2
#     elif isinstance(m2, tuple):
#         result2 = calculate(m2)
    
#     if op == "+":
#         return result1 + result2
#     elif op == "-":
#         return result1 - result2
#     elif op == "*":
#         return result1 * result2
#     elif op == "/":
#         return result1 / result2


def calculate(equation):
    if isinstance(equation, int):
        return equation

    m1, op, m2 = equation
    
    if isinstance(m1, int):
        result1 = m1
    elif isinstance(m1, tuple):
        result1 = calculate(m1)
    else:
        print(equation)
        assert False

    if isinstance(m2, int):
        result2 = m2
    elif isinstance(m2, tuple):
        result2 = calculate(m2)
    else:
        print(equation)
        assert False

    print("calculate", result1, result2)
    if op == "+":
        return result1 + result2
    elif op == "-":
        return result1 - result2
    elif op == "*":
        return result1 * result2
    elif op == "/":
        temp = result1 / result2
        if not (temp).is_integer():
            print(equation, temp)
            input()
        return int(temp)


def branch_has_x(branch):
    if isinstance(branch, int):
        return False
    if isinstance(branch, str) and branch == "x":
        return True
    m1, _, m2 = branch
    return branch_has_x(m1) or branch_has_x(m2)


def opposite_operand(op):
    if op == "+":
        return "-"
    if op == "-":
        return "+"
    if op == "/":
        return "*"
    if op == "*":
        return "/"


# (((4, '+', (2, '*', ('x', '-', 3))), '/', 4), '=', ((32, '-', 2), '*', 5))
def solve(equation):
    left, equals, right = equation    
    assert equals == "="
    if not branch_has_x(left):
        # x is on right. swap so that x is on left                    
        # example1: 10 - x, example2: 10 / x
        temp = left
        left = right
        right = temp

    if isinstance(left, str) and left == "x":
        return right
    
    assert isinstance(left, tuple)    
    left_m1, left_op, left_m2 = left

    if branch_has_x(left_m1):
        # example: x / 10 = right
        right = calculate((right, opposite_operand(left_op), left_m2))
        return solve((left_m1, equals, right))        
    else: # left_m2 has x
        # example: 10 / x = right
        if left_op == "/" or left_op == "-":
            right = (right, opposite_operand(left_op), left_m2) # right has x
            left_m1 = calculate(left_m1)
            return solve((right, equals, left_m1))
        right = calculate((right, opposite_operand(left_op), left_m1))
        return solve((left_m2, equals, right))

    # if not branch_has_x(left_m1):
    #     # x is on right. swap so that x is on left                    
    #     # example1: 10 - x = 
    #     # example2: 10 / x
    #     temp = left_m1
    #     left_m1 = left_m2
    #     left_m2 = temp
    #     # example1 swapped. now at x + 10
    #     if left_op == "-": # example: 10 - x => -x + 10
    #         left_m1 = (left_m1, '*', -1)
    #         left_op = '+'
    #         # no change to left_m2
    #     # example2 swapped. now at x / 10. should be at 1/x * 10
    #     if left_op == "/":
    #         left_op = "*"
    #         left_m1 = (1, "/", left_m1)
    #         # no change to left_m2
    # left_m2_result = calculate(left_m2)
    # right = calculate((right, opposite_operand(left_op), left_m2_result))
    # return solve((left_m1, "=", right))
    

result = int(find_root("root", monkeys))
print("part1", result)

result = find_root2("root", monkeys)
print(result)
# if not branch_has_x(result[0]):
#     result = (result[2], result[1], result[0])
result = solve(result)
print("part2", result)


# root - checks for equals =
# humn - is me