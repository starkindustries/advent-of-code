

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
                rules[number] = description
            else:
                messages.append(line)
    return rules, messages


# Sample rules:
# 0: 1 2
# 1: "a"
# 2: 1 3 | 3 1
# 3: "b"


def follow_rule(i, rules):

    rule = rules[i]
    # for rule in rules.values():
    if rule[0][0] in ['a', 'b']:
        # messages = [x.append(rule[0][0]) for x in messages]
        # print(rule[0][0])
        return [rule[0][0]]
    else:
        messages = []
        # Process one side at a time
        for side in rule:
            # process each rule in each side
            temp = ['']
            for side_rule in side:
                result = follow_rule(side_rule, rules)
                temp = [t + r for t in temp for r in result]
            messages.extend(temp)
        return messages


def solve_part1(filename):
    rules, messages = parse_input(filename)
    # print(rules)
    # print(messages)

    valid_messages = follow_rule(0, rules)
    # print("MESSAGES")
    # print(valid_messages)

    count = 0
    for m in messages:
        if m in valid_messages:
            count += 1
    print(f"Valid message count: {count}")
    return count
    # n = 0
    # while True:
    #     rule = rules[0]
    #     for item in rule:


assert solve_part1("sample1.txt") == 2
assert solve_part1("sample2.txt") == 2

solve_part1("input.txt")
