

def evaluate_part1(equation):
    equation = equation.replace(' ', '')
    result = None
    operand = None
    stack = []
    for i in range(len(equation)):
        if equation[i].isdigit():
            if result is None:
                result = int(equation[i])
            elif operand == "*":
                result *= int(equation[i])
            elif operand == "+":
                result += int(equation[i])
        elif equation[i] in ["*", "+"]:
            operand = equation[i]
        elif equation[i] == "(":
            stack.append((result, operand))
            result = None
            operand = None
        elif equation[i] == ")":
            if len(stack) > 0:
                r, o = stack.pop()
                if o is None:
                    pass
                elif o == "*":
                    result *= r
                elif o == "+":
                    result += r
    assert len(stack) == 0
    print(f"{equation} = {result}")
    return result


assert evaluate_part1("1 + 2 * 3 + 4 * 5 + 6") == 71
assert evaluate_part1("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert evaluate_part1("2 * 3 + (4 * 5)") == 26
assert evaluate_part1("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
assert evaluate_part1("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
assert evaluate_part1("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632
assert evaluate_part1("2 * (5 * ( 8 * ( 4 + 1 ) + 6) * 7)") == 3220
assert evaluate_part1("9 + 6 + (6 + 7 * 5 * 7 + 4 + 9) * (7 + (2 * 9 + 8 + 4 + 3 * 7) + 6 * 4 * (3 + 8 * 5 * 7) * 6) + ((3 * 4 * 4 + 3) + (4 + 7 + 6 + 6 + 5 + 2) + 6) * 8") == 8711620536
assert evaluate_part1("4 + ((1 + 2 * 2) * (2 + 4 * 7 + 5 * 3))") == 850


def add_then_multiply(stack):
    # Iterate through array and evaluation addition first
    # example: [(4, '*'), (4, '+'), (9, '*'), (3, None)]
    print(stack)
    i = 0
    while i < len(stack) - 1:
        num, operand = stack[i]  # ex: i = 1, r = 4, o = '+'
        if operand in ['(', ')']:
            raise RuntimeError(f"Unexpected operand {o} in stack: {stack} for equation: {equation}")
        elif operand == "+":
            num2, operand = stack.pop(i+1)    # r2 = 9, o = '*'
            stack[i] = (num + num2, operand)  # (4 + 9, *) => (13, *)        
        else:
            i += 1
    # Now evaluate multiplication
    result = 1
    for num, operand in stack:
        if num is not None:
            result *= num
    return result


# r is result
# o is operand
def evaluate_part2(equation):
    # 1 + 2 * 3 + 4 * 5 + 6
    # ^
    # 1 + 2 * 3 + 4 * 5 + 6
    #   3   *   7   * 11
    # s = [(3, *), (7, *)]
    # r = 11 * 7 * 3
    # o =
    # 3 * 3 + 4 * 5 + 6
    equation = equation.replace(' ', '')
    result = None
    operand = None
    stack = []
    for i in range(len(equation)):
        if equation[i].isdigit():
            if result is None:
                result = int(equation[i])
            elif operand == "*":
                stack.append((result, operand))
                result = int(equation[i])
                operand = None
            elif operand == "+":
                result += int(equation[i])
        elif equation[i] in ["*", "+"]:
            operand = equation[i]
        elif equation[i] == "(":
            stack.append((result, operand))
            stack.append((None, "("))
            result = None
            operand = None
        elif equation[i] == ")":
            temp_stack = [(result, None)]
            print(stack)
            print(f"operand: {operand}. result: {result}")
            num, operand = stack.pop()
            while operand != "(":
                temp_stack.insert(0, (num, operand))
                num, operand = stack.pop()
            result = add_then_multiply(temp_stack)
    stack.append((result, operand))

    # Iterate through stack and evaluation addition first
    # example: [(4, '*'), (4, '+'), (9, '*'), (3, None)]
    print(stack)
    return add_then_multiply(stack)
    # i = 0
    # while i < len(stack) - 1:
    #     r, o = stack[i]  # ex: i = 1, r = 4, o = '+'
    #     if o == "+":
    #         r2, o = stack.pop(i+1)  # r2 = 9, o = '*'
    #         stack[i] = (r + r2, o)  # (4 + 9, *) => (13, *)
    #     elif o in ['(', ')']:
    #         raise RuntimeError(f"Unexpected operand {o} in stack: {stack} for equation: {equation}")
    #     else:
    #         i += 1
    # # Now evaluate multiplication
    # result = 1
    # for r, o in stack:
    #     if r is not None:
    #         result *= r
    # return result


assert evaluate_part2("1 + 2 * 3 + 4 * 5 + 6") == 231
assert evaluate_part2("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert evaluate_part2("2 * 3 + (4 * 5)") == 46
assert evaluate_part2("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
assert evaluate_part2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
assert evaluate_part2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340
assert evaluate_part2("4 + ((1 + 2 * 2) * (2 + 4 * 7 + 5 * 3))") == 1300
assert evaluate_part2("4 * ((2 * 2) + (3 * 3))") == 52
assert evaluate_part2("4 * (2 * 2) + (3 * 3) * 3") == 156
assert evaluate_part2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340
assert evaluate_part2("(6 + 9 + 2 * (5 + 4 * 5)) * 4 + 9") == 9945
assert evaluate_part2("5 * (4 + 1) + (4 + 9 + 2) * 6") == 600
assert evaluate_part2("5 * (4 + 1) + ((4 * 9 + (2 + 1)) + 2) * 6") == 1650
assert evaluate_part2("7 * 3") == 21
assert evaluate_part2("5 + (4 * 1 + 5 * 4 + 1 * 2 + 2)") == 485
assert evaluate_part2("5 + (4 * 1 + (5 * 4) + 1 * 2 + 2)") == 357


def solve_part1(filename):
    with open(filename, 'r') as handle:
        puzzle_input = [line.strip() for line in handle]
    sum = 0
    for line in puzzle_input:
        sum += evaluate_part1(line)
    print(f"Part 1: {sum}")
    return sum


def solve_part2(filename):
    with open(filename, 'r') as handle:
        puzzle_input = [line.strip() for line in handle]
    sum = 0
    for line in puzzle_input:
        sum += evaluate_part2(line)
    print(f"Part 2: {sum}")
    return sum


assert solve_part1("input.txt") == 30753705453324
assert solve_part2("input.txt")
