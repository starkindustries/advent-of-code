


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


def follow_rule(i, rules):
    # valid_messages = []
    return follow_helper(i, rules)

# 0: 1 2
# 1: "a"
# 2: 1 3 | 3 1
# 3: "b"

# i = 1
# messages = [a,]
def follow_helper(i, rules):
    rule = rules[i]
    # for rule in rules.values():
    if len(rule) == len(rule[0]) == 1 and rule[0][0] in ['a', 'b']:
        # messages = [x.append(rule[0][0]) for x in messages]
        print(rule[0][0])
    elif len(rule) == 1:
        for r in rule[0]:
            follow_helper(r, rules)
    else: # len(rules) == 2
        print(f"SEPARATOR")
        for sub in rule: # rule = 1 3 | 3 1
            for j in sub: # sub = 1 3
                follow_helper(j, rules)
            print("** OR **")
    return -1


def solve_part1(filename):
    rules, messages = parse_input(filename)
    print(rules)
    print(messages)

    valid_messages = follow_rule(0, rules)
    # n = 0
    # while True:
    #     rule = rules[0]
    #     for item in rule:


solve_part1("sample1.txt")
print(f"=============================")
solve_part1("sample2.txt")

# assert solve_part1("sample1.txt") == 2
