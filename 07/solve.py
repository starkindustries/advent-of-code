# Format {"inside bag" : "container bag"}
# {"shiny gold" : [(3, "muted yellow"), (2, "light red")]}

# inside:outside bag rules (part 1)
rules = {}
# outside: inside bag rules (part 2)
rules2 = {}
with open("input.txt", 'r') as handle:    
    for line in handle:
        line = line.strip()
        # split the container from its contents
        container, contents = line.split(" contain ")        
        # drop the period '.' and split on the command ','
        contents = contents[:-1].split(", ")
        # drop the 'bags'
        container = container.replace(' bags', '')
        contents = [c.replace(' bags', '').replace(' bag', '') for c in contents]
        for c in contents:
            try:
                number = int(c[:2])
                bag = c[2:]
                # print(f"#, bag: {number}, {bag}")
                rules[bag] = rules.get(bag, [])
                rules[bag].append(container)

                # rules part 2
                rules2[container] = rules2.get(container, [])
                rules2[container].append((bag, number))
            except:
                # Contain no other bags
                rules2[container] = rules2.get(container, [])
                pass
        # print(f"{container} || {contents}")

# print(f"Rules: {rules}")
# process rules
queue = ["shiny gold"]
containers = set()
while len(queue) > 0:
    bag = queue.pop()
    if bag in rules:
        containers.update(rules[bag])
        queue.extend(rules[bag])
# print(f"Containers: {sorted(containers)}")
print(f"Total count: {len(containers)}")

# part 2
def getTotalBags(bag):
    total = 0
    for insideBag, number in rules2[bag]:
        total += number + number * getTotalBags(insideBag)
    return total

print(f"rules2: {rules2}")
total = getTotalBags("shiny gold")
print(f"Total bags: {total}")