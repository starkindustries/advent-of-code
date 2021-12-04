def parse_rule(line):
    number, temp_description = line.split(":")
    number = int(number)
    description = []
    for sub_rule in temp_description.split("|"):
        sub_rule = sub_rule.strip()
        items = []
        for item in sub_rule.split(' '):
            item = item.replace('"', '')
            if item.isdigit():
                item = int(item)
            items.append(item)
        description.append(items)
    return number, description


def parse_input(filename):
    read_rules = True
    rules = {}
    messages = []
    with open(filename, 'r') as handle:
        for line in handle:
            line = line.strip()
            if line == '':
                read_rules = False
            elif read_rules:
                number, description = parse_rule(line)
                rules[number] = description
            else:
                messages.append(line)
    return rules, messages


# Sample looping rule set
# 0: 3 4
# 1: "a"
# 2: "b"
# 3: 1 | 1 3
# 4: 2 | 2 4
def rule_dfs(message, m_index, r, rules):
    if not r:  # if rules array is empty
        return m_index == len(message)
    # if rules array is not empty and m_index >= len(message)
    if m_index >= len(message):
        return False

    # evaluate only the first rule given

    # If rule has options
    # ex: r = [3, 4] ==> len(rules[r[0]]) = len(rules[3]) = len([[1], [1, 3]]) = 2
    if len(rules[r[0]]) == 2:
        # rules[r[0]][0] = rules[3][0] = [[1], [1, 3]][0] = [1]
        # r[1:] = [3, 4][1:] = [4]
        # new1 = [1] + [4] = [1, 4]
        new1 = rules[r[0]][0] + r[1:]
        # rules[r[0]][1] = rules[3][1] = [[1], [1, 3]][1] = [1, 3]
        # r[1:] = [3, 4][1:] = [4]
        # new2 = [1, 3] + [4] = [1, 3, 4]
        new2 = rules[r[0]][1] + r[1:]
        return rule_dfs(message, m_index, new1, rules) or rule_dfs(message, m_index, new2, rules)
    # If rule is a base case 'a' or 'b'
    # ex: r = [1, 4] ==> rules[r[0]][0][0] = rules[1][0][0] = [['a']][0][0] = ['a'][0] = 'a'
    elif (letter := rules[r[0]][0][0]) in ['a', 'b']:
        if message[m_index] == letter:
            r.pop(0)
            return rule_dfs(message, m_index+1, r, rules)
        return False
    # If rule is a sequence w/o options
    else:
        # Similar to case with options, just without the 2nd new rule
        new = rules[r[0]][0] + r[1:]
        return rule_dfs(message, m_index, new, rules)


def solve(filename, replacement_rules=[]):
    rules, messages = parse_input(filename)

    for line in replacement_rules:
        number, description = parse_rule(line)
        rules[number] = description

    count = 0
    for m in messages:
        # print(f"Checking message {m} against rules: {rules[0][0]}")
        result = rule_dfs(m, 0, rules[0][0].copy(), rules)
        if result:
            # print(f"Validated message: {m}")
            count += 1

    print(f"Valid message count: {count}")
    return count


assert solve("sample1.txt") == 2
assert solve("sample2.1.txt") == 0
assert solve("sample2.txt") == 2
assert solve("sample3.1.txt") == 1
assert solve("sample3.txt") == 8

# Part 1
print("Part 1")
assert solve("input.txt") == 291

# Part 2
# Replace rules 8 and 11 with the following:
# 8: 42 | 42 8
# 11: 42 31 | 42 11 31
print("Part 2")
assert solve("input.txt", ["8: 42 | 42 8", "11: 42 31 | 42 11 31"]) == 409
