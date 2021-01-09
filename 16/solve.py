import pytest

DEBUG = False

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

# Check if the target 'n' is valid for any of the given rules
def test_rules(n, rules):
    for _, rule in rules.items():
        for lower_range, upper_range in rule:
            if lower_range <= n <= upper_range:
                return True                
    return False

def solve_part1(filename):
    rules, _, nearby_tickets = parse_input(filename)

    error_rate = 0
    for ticket in nearby_tickets:
        for n in ticket:
            if not test_rules(n, rules):
                error_rate += n
    return error_rate

# rules 0, 1, 2 
# rules: {'class': [[ 1,  3], [ 5,  7]],
#         'row':   [[ 6, 11], [33, 44]], 
#         'seat':  [[13, 40], [45, 50]]}

#                      
# valid tickets: [[ 7, 3, 47], 
#                 [40, 4, 50], 
#                 [55, 2, 20]]
def valid_rule_for_column(rules, rule_index, tickets, ticket_column):
    for ticket in tickets:
        ticket_is_valid = False
        for lower_range, upper_range in rules[rule_index]:
            if lower_range <= ticket[ticket_column] <= upper_range:
                # the column for this ticket is valid for this rule
                ticket_is_valid = True
                break
        if not ticket_is_valid:
            return False
    return True

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
        
    rules_order = [column[0] for column in rules_to_columns]    
    if DEBUG:
        print(f"rules order: {rules_order}")                    
        print(f"my ticket: {my_ticket}")    

    solution = 1
    keys = list(rules.keys())
    for rule_index, ticket_index in enumerate(rules_order):
        if "departure" in keys[rule_index]:
            solution *= my_ticket[ticket_index]
            if DEBUG:
                print(f"{keys[rule_index]}: {my_ticket[ticket_index]}. solution: {solution}")
    return solution

# Test valid_rule_for_column()
rule = [[[0,1],[4,19]]]
tickets = [[3,9,18],[15,1,5],[5,14,9]]
assert valid_rule_for_column(rule, 0, tickets, 0) == False
assert valid_rule_for_column(rule, 0, tickets, 1) == True
assert valid_rule_for_column(rule, 0, tickets, 2) == True

rule = [[[0,5],[8,19]]]
assert valid_rule_for_column(rule, 0, tickets, 0) == True
assert valid_rule_for_column(rule, 0, tickets, 1) == True
assert valid_rule_for_column(rule, 0, tickets, 2) == True
assert valid_rule_for_column(rule, 0, [[6]], 0) == False
assert valid_rule_for_column(rule, 0, [[7]], 0) == False
assert valid_rule_for_column(rule, 0, [[20]], 0) == False

# Known solutions
assert solve_part1("sample.txt") == 71
assert solve_part1("input.txt") == 22057
assert solve_part2("input.txt") == 1093427331937

print(f"Part 1: {solve_part1('input.txt')}")
print(f"Part 2: {solve_part2('input.txt')}")