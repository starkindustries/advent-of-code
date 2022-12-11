

def solve():
    pass


# { 
#   "items" : {
#       {1: (79, %r)}
#       2: (102, %r)    
#   },
#   "operation" : [ "*", 19 ],
#   "test" : 23,
#   "true" : 2,
#   "false" : 3
#   "count" = 0
# }

monkeys = []
item_index = 0

filename = "input.txt"
with open(filename, 'r') as handle:
    while True:        
        # monkey index
        line = handle.readline()
        if line == "":
            break
        index = int(line.split()[1][:-1])
        monkeys.append({ "count" : 0 })
        # starting
        line = handle.readline()
        numbers = line.split(":")[1]
        numbers = list(map(int, numbers.split(",")))
        monkeys[index]["items"] = numbers
        #monkeys[index]["items"] = {}
        #for num in numbers:
        #    monkeys[index]["items"][item_index] = num
        #    item_index += 1        
        # operation
        line = handle.readline()
        line = line.split("=")[1].split()
        monkeys[index]["operation"] = [line[1], line[2]]
        # test
        line = handle.readline()
        monkeys[index]["test"] = int(line.split("by")[1])
        # true
        line = handle.readline()
        monkeys[index]["true"] = int(line.split("monkey")[1])
        # false
        line = handle.readline()
        monkeys[index]["false"] = int(line.split("monkey")[1])
        # read in blank line
        line = handle.readline().strip()
        assert line == ""

lcm = 1
mod_lookup = {}
for m in monkeys:
    print(m)
    mod_lookup[m["test"]] = {}
    lcm *= m["test"]

#thrown_items = [[] for x in range(len(monkeys))]
# print("thrown_items", thrown_items)
rounds = 10000
for _ in range(rounds):
    for monkey in monkeys:
        # Monkey inspects an item with a worry level of 79        
        while len(monkey["items"]) > 0:
            
            item = monkey["items"].pop(0)
             #print("item", item, type(item))   
            monkey["count"] += 1
            # Worry/item level is multiplied by 19 to 1501                        
            if monkey["operation"][0] == "*":
                if monkey["operation"][1] == "old":
                    item *= item
                else:
                    item *= int(monkey["operation"][1])
            elif monkey["operation"][0] == "+":
                if monkey["operation"][1] == "old":
                    item += item
                    # print("item", item, type(item))   
                else:
                    item += int(monkey["operation"][1])
            # Monkey gets bored with item. Worry level is divided by 3 to 500
            # print("item", item, type(item))           
            # if item % 96577 == 0:
            # WORRY DIVISOR
            # item = item // 3
            # Current worry level is not divisible by 23            
            # modulo = monkey["test"]
            # remainder = item % modulo            
            # if remainder in mod_lookup[modulo]:
            #     if mod_lookup[modulo][remainder] < item:
            #         item = mod_lookup[modulo][remainder]
            #     elif mod_lookup[modulo][remainder] > item:
            #         mod_lookup[modulo][remainder] = item
            # else:
            #     mod_lookup[modulo][remainder] = item            

            #mod_lookup[monkey["test"]].append((item, item % monkey["test"]))
            
            modulo = monkey["test"]
            test_result = item % modulo
            if item > lcm:                                
                remainder = item % lcm
                item = lcm + remainder

            if test_result == 0:
                # item = item // monkey["test"]
                index = monkey["true"]
                # print("index", index, thrown_items)
                #thrown_items[index].append(item)
            else:
                # Item with worry level 500 is thrown to monkey 3.
                index = monkey["false"]
                # print("index", index, thrown_items)
            monkeys[index]["items"].append(item)

    # print()
    # print("Round", round)
    # for m in monkeys:
    #     temp = m.copy()
    #     temp["items"] = len(temp["items"])
    #     print(temp)    
    #temp = 1
    # At end of round, append all thrown items to the monkeys
    # for index, items in enumerate(thrown_items):
    #     monkeys[index]["items"].extend(items)

print()
counts = []
for i, m in enumerate(monkeys):
    counts.append(m["count"])
    print(f"[{i}]: { m['count'] } ")

counts.sort()
answer = counts.pop() * counts.pop()
print("part1", answer)


# (79 * 19 - 6) / 23 = 65
# 
#### PART 2
# rounds = 10000
# for _ in range(rounds):
#     for monkey in monkeys:
#         # Monkey inspects an item with a worry level of 79        
#         monkey["count"] += len(monkey["items"])
#         if monkey["operation"][0] == "*":ex
#             if monkey["operation"][1] == "old":
#                 monkey["items"] = [x * x for x in monkey["items"]]
#             else:
        
#         while len(monkey["items"]) > 0:            
#             item = monkey["items"].pop(0)
#              #print("item", item, type(item))   
#             monkey["count"] += 1
#             # Worry/item level is multiplied by 19 to 1501                        
#             if monkey["operation"][0] == "*":
#                 if monkey["operation"][1] == "old":
#                     item *= item
#                 else:
#                     item *= int(monkey["operation"][1])
#             elif monkey["operation"][0] == "+":
#                 if monkey["operation"][1] == "old":
#                     item += item
#                     # print("item", item, type(item))   
#                 else:
#                     item += int(monkey["operation"][1])
#             # Monkey gets bored with item. Worry level is divided by 3 to 500
#             # print("item", item, type(item))           
#             item = item // 3
#             # Current worry level is not divisible by 23
#             if item % monkey["test"] == 0:
#                 index = monkey["true"]
#                 # print("index", index, thrown_items)
#                 #thrown_items[index].append(item)
#             else:
#                 # Item with worry level 500 is thrown to monkey 3.
#                 index = monkey["false"]
#                 # print("index", index, thrown_items)
#             monkeys[index]["items"].append(item)

# print("*** TEST ***")

# def calculate(num, monkey):
#     if monkey == 0:
#         num *= 19
#         if num % 23 == 0:
#             print(f"{num} divisible by 23!")
#             input()
#             return num, 2
#         return num, 3
#     # monkey 1
#     if monkey == 1:
#         num += 6
#         if num % 19 == 0:
#             print(f"{num} divisible by 19!")
#             input()
#             return num, 2
#         return num, 0
#     # monkey 2
#     if monkey == 2:
#         num *= num
#         if num % 13 == 0:
#             print(f"{num} divisible by 13!")
#             input()
#             return num, 1
#         return num, 3
#     # monkey 3
#     if monkey == 3:
#         num += 3
#         if num % 17 == 0:
#             print(f"{num} divisible by 17!")
#             input()
#             return num, 0
#         return num, 1
#     assert False

# lcm = 17 * 13 * 19 * 23
# num = 79
# monkey = 0
# while True:
#     num, monkey = calculate(num, monkey)
#     if num % lcm == 0:
#         print(f"{num} divisible by LCM {lcm}!")
#         input()