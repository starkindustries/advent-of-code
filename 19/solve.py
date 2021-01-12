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


# class Node:
#     def __init__(letter=None):
#         self.letter = letter
#         self.left = None
#         self.right = None


# def create_rule_tree(i, rules):
#     my_tree = Node()
#     tree_helper(i, rules, my_tree)
#     return my_tree

# #    a
# #  a   b
# # a b
# def tree_helper(i, rules, node):
#     rule = rules[i]
#     if rule[0][0] in ['a', 'b'] and node.letter is None:
#         node.letter = rule[0][0]
#     else:
#         # Process one side at a time
#         for side in rule:
#             # process each rule in each side
#             for side_rule in side:
#                 if node.left is None:
#                     node.left = Node()
#                     node = node.left
#                     tree_helper(side_rule, rules, node)
#                 else:
#                     node.right = Node()
#                     node = node.right
#                     tree_helper(side_rule, rules, node)
    # result = follow_rule(side_rule, rules)
    # temp = [t + r for t in temp for r in result]
    # messages.extend(temp)
    # return messages


# Sample rules:
# 0: 1 2
# 1: "a"
# 2: 1 3 | 3 1
# 3: "b"

# if m_index == len(message):
# return true
# if rule is 'a':
#    check if 'a' matches current index
# same with 'b'
# if just one rule:
# for num in rule:
#     follow rule.  # e.g. for rule 0
# if two rules
# return follow(left) or follow(right)
#
def rule_dfs(message, m_index, rules, r_index):
    rule = rules[r_index]
    if m_index >= len(message):
        return False
    if rule[0][0] in ['a', 'b']:
        return rule[0][0] == message[m_index]
    # case where rule contains one option e.g. 0: 1 2
    # or if left side true, don't need to check the right
    left_side = rule[0]    
    left_valid = True
    for i, sub_rule in enumerate(left_side):
        if not rule_dfs(message, m_index + i, rules, sub_rule):
            left_valid = False
            break
    if len(rule) == 1 or left_valid:
        return left_valid
    # case where rule has an 'or' case e.g. 2: 1 3 | 3 1
    print(f"RULE: {rule}. len: {len(rule)}")
    right_side = rule[1]
    for i, sub_rule in enumerate(right_side):
        if not rule_dfs(message, m_index + i, rules, sub_rule):
            return False
    return True

# v
# bbb
#

# def follow_rule(i, rules):
#     rule = rules[i]
#     if rule[0][0] in ['a', 'b']:
#         return [rule[0][0]]
#     else:
#         messages = []
#         # Process one side at a time
#         for side in rule:
#             # process each rule in each side
#             temp = ['']
#             for side_rule in side:
#                 result = follow_rule(side_rule, rules)
#                 temp = [t + r for t in temp for r in result]
#             messages.extend(temp)
#         return messages


def solve_part1(filename):
    rules, messages = parse_input(filename)
    # valid_messages = follow_rule(0, rules)

    # create_rule_tree(0, rules)
    # print(f"Tree completed")
    # exit()
    # print(f"Length of valid msgs: {len(valid_messages)}")
    # print(f"valid messages: {valid_messages}")
    count = 0
    for m in messages:
        count += 1 if rule_dfs(m, 0, rules, 0) else 0
    print(f"Valid message count: {count}")
    return count


def solve_part2(filename):
    rules, messages = parse_input(filename)

    # Replace rules 8 and 11 with the following:
    # 8: 42 | 42 8
    # 11: 42 31 | 42 11 31
    for line in ["8: 42 | 42 8", "11: 42 31 | 42 11 31"]:
        number, description = parse_rule("8: 42 | 42 8")
        rules[number] = description
    valid_messages = follow_rule(0, rules)


assert solve_part1("sample1.txt") == 2
assert solve_part1("sample2.txt") == 2
assert solve_part1("input.txt") == 291

# solve_part2("input.txt")
