import string


# Part 1
alphabet = list(string.ascii_lowercase)
alphabet += list(string.ascii_uppercase)

value = 1
priority_values = {}
for letter in alphabet:
    priority_values[letter] = value
    value += 1

priority_score = 0
filename = "input.txt"

with open(filename, 'r') as handle:
    for line in handle:                
        rucksack = line.strip()
        half_len = int(len(rucksack)/2)
        one = rucksack[:half_len]
        two = rucksack[half_len:]
        
        
        table = {}
        for char in one:
            table[char] = 1
        for char in two:
            if char in table:
                value = priority_values[char]
                print(f"{one} : {two} : {char} : {value}")
                priority_score += value
                break
print("Part 1 priority score:", priority_score)


# Part 2
score2 = 0

with open(filename, 'r') as handle:    
    group_member = 0
    # { 'letter' : [x, y, z]}
    # x, y, z should each be set to true to test if all elves have item
    table = {}
    for line in handle:
        rucksack = line.strip()
        for char in rucksack:
            table.setdefault(char, [False, False, False])
            table[char][group_member] = True
        group_member += 1
        if group_member == 3:
            for key, val in table.items():
                if val[0] == val[1] == val[2] == True:
                    badge = key
                    break
            value = priority_values[badge]            
            print(table)
            print(f"{badge} : {value}")
            score2 += value
            group_member = 0
            table = {}
print("Part 2 priority:", score2)