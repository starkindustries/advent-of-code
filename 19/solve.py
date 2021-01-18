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

def rule_dfs(message, rules):
    result, index = rule_dfs_helper(message, 0, rules, 0)
    if result and index == len(message):
        return True
    return False

# use message to keep track of index
def rule_dfs_helper(message, m_index, rules, r_index, r_next=None):
    # print(f"RINDEX: {r_index}")
    # rule = rules[r_index]    
    
    # Exit case
    if m_index > len(message):
        # if m_index is greater than message length then
        # the function is trying to check a letter that
        # is out of range, which does not satisfy the rules
        return False, -1
    elif m_index == len(message):
        return True, m_index
        
    if isinstance(r_index, list):
        rule = [r_index]
    else:
        rule = rules[r_index]
    print(f"M:{message} @ {m_index}. R:{rule}")

    # Test each side of the rule: e.g. [1 3] or [3 1]
    # TODO: STOPPED HERE ==> SHOULD RETURN TRUE ONLY IF CURRENT RULE AND NEXT RULE ARE TRUE
    if len(rule) == 2:
        r1, i1 = rule_dfs_helper(message, m_index, rules, rule[0])        
        if r_next:
            r2, i2 = rule_dfs_helper(message, i1, rules, r_next, None)
            if (r1 and r2):
                return True, i2
        elif r1:
            return True, i1
        r3, i3 = rule_dfs_helper(message, m_index, rules, rule[1])
        if r_next:
            r4, i4 = rule_dfs_helper(message, i3, rules, r_next, None)
            if (r3 and r4):
                return True, i4
        elif r3:
            return True, i3
        return False, -1

    assert len(rule) == 1
    
    # Iterate through each sub rule e.g. [1, 3]
    side_valid = True
    index = m_index
    for i in range(len(rule[0])):
        sub_rule = rule[0][i]
        if sub_rule in ['a', 'b']:
            result = (sub_rule == message[index])
            index += 1
        elif i+1 < len(rule[0]):
            result, index = rule_dfs_helper(message, index, rules, sub_rule, rule[0][i+1])
        else:
            result, index = rule_dfs_helper(message, index, rules, sub_rule, None)
        if not result:
            side_valid = False
            break
    return side_valid, index

    # exit()
    
    # left_side = rule[0]
    # left_valid = True
    # for i, sub_rule in enumerate(left_side):
    #     # TODO: STOPPED HERE.. Need to fix m_index vs new_index. 
    #     # cause when you traverse one rule, you could add +inf letters
    #     # then the next rule's message index WILL NOT be m+1
    #     result, new_index = rule_dfs(message, new_index, rules, sub_rule)
    #     if not result:
    #         left_valid = False
    #         break
    # if len(rule) == 1 or left_valid:
    #     return left_valid, new_index+1
    # # case where rule has an 'or' case e.g. 2: 1 3 | 3 1
    # print(f"RULE: {rule}. len: {len(rule)}")
    # right_side = rule[1]
    # for i, sub_rule in enumerate(right_side):
    #     result, new_index = rule_dfs(message, m_index + i, rules, sub_rule)
    #     if not result:
    #         return False, new_index+1
    # return True, new_index+1

# v
# bbb
#

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
    # valid_messages = follow_rule(0, rules)

    # create_rule_tree(0, rules)
    # print(f"Tree completed")
    # exit()
    # print(f"Length of valid msgs: {len(valid_messages)}")
    # print(f"valid messages: {valid_messages}")
    count = 0
    for m in messages:        
        result = rule_dfs(m, rules)
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

    # messages42 = follow_rule(31, rulinputes)
    # print(messages42)
    # exit()

    count = 0
    for m in messages:
        result = rule_dfs(m, rules)
        if result: 
            print(f"P2: validated message: {m}")
            count += 1

    print(f"Part 2: valid message count: {count}")
    return count


# assert solve_part1("sample1.txt") == 2
# assert solve_part1("sample2.1.txt") == 0
# assert solve_part1("sample2.txt") == 2
# assert solve_part1("input.txt") == 291

assert solve_part1("sample3.txt") == 8

solve_part2("input.txt")
