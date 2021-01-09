import pytest

DEBUG = True

# Test a single rule
def test_rule(n, rule):
    for lower_range, upper_range in rule:
        if lower_range <= n <= upper_range:
            return True
    return False

# Check if the target 'n' is valid for any of the given rules
def test_rules(n, rules):
    for _, rule in rules.items():
        if test_rule(n, rule):
            return True
    return False

def parse_input(filename):
    puzzle_input = []
    with open(filename, 'r') as handle:
        puzzle_input = [line.strip() for line in handle if line.strip() != '']    
    
    ticket_index = puzzle_input.index("your ticket:")
    
    rules = {}
    for r in puzzle_input[0:ticket_index]:        
        name, ranges = r.split(":")
        ranges = [list(map(int, ticket_range.split("-"))) for ticket_range in ranges.split(" or ")]
        rules[name] = ranges
    ticket_info = [int(n) for n in puzzle_input[ticket_index+1].split(",")]
    nearby_tickets = [list(map(int, ticket.split(","))) for ticket in puzzle_input[ticket_index+3:]]

    if DEBUG:
        print(f"ticket index: {ticket_index}")
        print(f"rules: {rules}")    
        print(f"ticket info: {ticket_info}")
        print(f"nearby: {nearby_tickets}")

    return rules, ticket_info, nearby_tickets

def solve_part1(filename):
    rules, _, nearby_tickets = parse_input(filename)

    error_rate = 0
    for ticket in nearby_tickets:
        for n in ticket:
            if not test_rules(n, rules):
                error_rate += n
    return error_rate

# depth first search
# def dfs(rules, tickets):
#     dfs_helper(rules.values(), tickets, [])

# rules 0, 1, 2 
# rules: {'class': [[ 1,  3], [ 5,  7]],
#         'row':   [[ 6, 11], [33, 44]], 
#         'seat':  [[13, 40], [45, 50]]}

#                      
# valid tickets: [[ 7, 3, 47], 
#                 [40, 4, 50], 
#                 [55, 2, 20]]

def valid_rule_for_column(rules, rule_index, tickets, ticket_column, rules_to_columns={}):
    key = str(rule_index) + ":" + str(ticket_column)
    if key in rules_to_columns:
        # print(f"key found: {key}: {rules_to_columns[key]}")
        return rules_to_columns[key]
    for ticket in tickets:
        ticket_is_valid = False
        for lower_range, upper_range in rules[rule_index]:
            if lower_range <= ticket[ticket_column] <= upper_range:
                # the column for this ticket is valid for this rule
                ticket_is_valid = True                
                break
        if not ticket_is_valid:
            rules_to_columns[key] = False
            return False
    rules_to_columns[key] = True
    return True

rule = [[[0,1],[4,19]]]
tickets = [[3,9,18],[15,1,5],[5,14,9]]
assert valid_rule_for_column(rule, 0, tickets, 0) == False
assert valid_rule_for_column(rule, 0, tickets, 1) == True
assert valid_rule_for_column(rule, 0, tickets, 2) == True

rule = [[[0,5],[8,19]]]
assert valid_rule_for_column(rule, 0, tickets, 0, {}) == True
assert valid_rule_for_column(rule, 0, tickets, 1) == True
assert valid_rule_for_column(rule, 0, tickets, 2) == True
assert valid_rule_for_column(rule, 0, [[6]], 0) == False
assert valid_rule_for_column(rule, 0, [[7]], 0) == False
assert valid_rule_for_column(rule, 0, [[20]], 0) == False

# rules:  [0, 1, 2, 3, 4, 5]
# ticket: [0, 2, 1, 4, 5, 3]
def dfs_helper(graph, rules_order, rules_to_columns):
    # if len(rules_order) == len(rules_to_columns):
    #     print(f"SOLVED Rules order: {rules_order}...")
    #     # exit()
    #     return rules_order
    # Visit node
    # rule_index = rules_order[-1]
    # ticket_column = len(rules_order)
    # if not rule_is_valid(rules[rule_index], tickets, ticket_column):
    #     return
    
    # print(f"Visited: {rules_order}")
    # Mark node as visited
    # visited[vertex] = True

    # Visit remaining nodes
    for column_index in graph:
        # visit adjacent nodes that are valid
        if column_index not in rules_order and column_index in rules_to_columns[len(rules_order)]:
        # if index not in rules_order and valid_rule_for_column(rules, index, tickets, len(rules_order), rules_to_columns):
            # new_rules = rules_order.copy()
            # new_rules.append(index)
            rules_order.append(column_index)            
            dfs_helper(graph, rules_order, rules_to_columns)
            if len(rules_order) == len(rules_to_columns):
                return rules_order
            rules_order.pop()
            # print(f"popped: {popped}")
    # return rules_order

# print(f"DFS")
# test_input = [0, 1, 2, 3, 4, 5]
# dfs_helper(test_input, [0], [], [])
# exit()

# def dfs_helper(rules, tickets, queue):
#     if not queue:
#         # queue is empty. add any valid rules
#         print(f"rules: {rules}")
#         for rule_index, rule in enumerate(rules):
#             for col in range(len(tickets[0])):
#                 is_valid = True
#                 for row in range(len(tickets)):
#                     if not test_rule(tickets[row][col], rule):
#                         is_valid = False
#                         break
#                 if is_valid:        
#                     queue.append([(col, rule_index)])
        
#     for item in queue:


    # check if rules valid
    # for 
    # if valid return order


def solve_part2(filename):
    rules, my_ticket, nearby_tickets = parse_input(filename)

    valid_tickets = []
    for ticket in nearby_tickets:
        is_valid = True
        for n in ticket:
            if not test_rules(n, rules):
                # invalid ticket
                is_valid = False
                break
        if is_valid:
            valid_tickets.append(ticket)
    
    if DEBUG:
        print(f"valid tickets: {valid_tickets}")          

    print(f"rules: {rules}")
    
    # Find all valid columns for each rule:
    rule_values = list(rules.values())
    rules_to_columns = [[] for i in range(len(rules))]
    for i in range(len(rules)):
        for column in range(len(valid_tickets[0])):
            if valid_rule_for_column(rule_values, i, valid_tickets, column):
                rules_to_columns[i].append(column)
    
    # Narrow down rules with only 1 possible column
    visited = []
    while True:
        # Find a rule with only a single valid column
        new_column_found = False
        for valid_columns in rules_to_columns:
            if len(valid_columns) == 1 and valid_columns[0] not in visited:                
                visited.append(valid_columns[0])                                                           
                new_column_found = True
                break
        if not new_column_found:
            break
        # Remove the found column for all other rules
        for valid_columns in rules_to_columns:
            if len(valid_columns) > 1 and visited[-1] in valid_columns:
                valid_columns.remove(visited[-1])
    for i, r in enumerate(rules_to_columns):
        print(f"{i}: {r}")
    # exit()

    rules_order = dfs_helper(range(len(rules)), [], rules_to_columns)
            
    


    # print(rules_to_columns)
    print(f"SOLUTION: {rules_order}")    

    # names = list(rules.keys())
    # # Get a list of all rules that are valid for the first column    
    # # valid_rules_for_first_column = []
    # rules = list(rules.values())
    # # for i in range(len(rules)):
    # #     print(f"RULES= {rules[i]}")
    # #     if valid_rule_for_column(rules[i], valid_tickets, 0):
    # #         valid_rules_for_first_column.append(i)
    # graph = range(len(rules))    

    # rules_to_columns = {}
    # rules_order = dfs_helper(graph, [], rules, valid_tickets, rules_to_columns)
    # print(f"SOLVED {rules_order}")
    # # Iterate through all of these possible starting nodes
    # for first_col_rule in valid_rules_for_first_column:
    #     rules_order = dfs_helper(graph, [first_col_rule], rules, valid_tickets)
    #     # Verify that all the rules are there
    #     if len(rules_order) == len(rules):
    #         print(f"Solved! {rules_order}")
    #         return
        # Verify that the rules are in fact correct
        # valid = True
        # for ticket_index, rule_index in enumerate(rules_order):
        #     if not valid_rule_for_column(rules[rule_index], valid_tickets, ticket_index):
        #         print(f"Error: invalid rule found {rules[rule_index]} for ticket column: {ticket_index}")
        #         valid = False
        #         break
        # if valid:
        #     print(f"Solved! {rules_order}")
        #     return

    print(f"RRR{rules}")
    print(f"*********** {my_ticket} **************")
    # exit()

    solution = 1
    keys = list(rules.keys())
    for rule_index, ticket_index in enumerate(rules_order):
        if "departure" in keys[rule_index]:
            solution *= my_ticket[ticket_index]
            print(f"{keys[rule_index]}: {my_ticket[ticket_index]}. solution: {solution}")
    print(f"Part 2 solution: {solution}")


# assert solve_part1("sample.txt") == 71
# result = solve_part1("input.txt")
# print(f"Part 1: {result}")
solve_part2("input.txt")

# 486854505461
# 233401847267