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


# Sample recursive rule set
# 0: 3 4
# 1: "a"
# 2: "b"
# 3: 1 | 1 3
# 4: 2 | 2 4
def rule_dfs(message, m_index, r, rules):
    if not r:
        return m_index == len(message)
    if m_index >= len(message):
        return False

    # evaluate the first rule given
    # print(f"M:{message}:{m_index}. R:{r}")
    if len(rules[r[0]]) == 2:  # if rule has options
        new1 = rules[r[0]][0].copy()
        new1.extend(r[1:])

        new2 = rules[r[0]][1].copy()
        new2.extend(r[1:])
        return rule_dfs(message, m_index, new1, rules) or rule_dfs(message, m_index, new2, rules)
    elif (letter := rules[r[0]][0][0]) in ['a', 'b']:
        if message[m_index] == letter:
            r.pop(0)
            return rule_dfs(message, m_index+1, r, rules)
        return False
    else:
        new = rules[r[0]][0].copy()
        new.extend(r[1:])
        return rule_dfs(message, m_index, new, rules)


def solve_part1(filename):
    rules, messages = parse_input(filename)
    count = 0
    for m in messages:
        print(f"Checking message {m} against rules..")
        result = rule_dfs(m, 0, rules[0][0], rules)
        if result:
            print(f"Validated message: {m}")
            count += 1
    print(f"Part 1: valid message count: {count}")
    return count


def solve_part2(filename):
    rules, messages = parse_input(filename)

    # Replace rules 8 and 11 with the following:
    # 8: 42 | 42 8
    # 11: 42 31 | 42 11 31
    for line in ["8: 42 | 42 8", "11: 42 31 | 42 11 31"]:
        number, description = parse_rule(line)
        rules[number] = description

    count = 0
    for m in messages:
        result = rule_dfs(m, 0, rules[0][0], rules)
        if result:
            print(f"P2: validated message: {m}")
            count += 1

    print(f"Part 2: valid message count: {count}")
    return count


# assert solve_part1("sample1.txt") == 2
# assert solve_part1("sample2.1.txt") == 0
# assert solve_part1("sample2.txt") == 2
# assert solve_part1("input.txt") == 291

assert solve_part1("sample3.1.txt") == 1
assert solve_part1("sample3.txt") == 8

solve_part2("input.txt")
