

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
    if rule[0][0] in ['a', 'b']:
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

    valid_messages = follow_rule(0, rules)

    count = 0
    for m in messages:
        if m in valid_messages:
            count += 1
    print(f"Valid message count: {count}")
    return count


assert solve_part1("sample1.txt") == 2
assert solve_part1("sample2.txt") == 2

solve_part1("input.txt")
