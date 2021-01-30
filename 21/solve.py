# parse items
# add items to dictionary of { allergen: possible_ingredients }
# if allergen is already in dictionary,
# do an intersection between the current input and the dictionary value
# if the dictionary value has just 1 item, remove that value from all 
# other allergens' possible values if exists
def solve(filename):
    allergen_dict = {}  # { allergen : possible_ingredients }    
    ingredient_count = {}  # { ingredient : count }

    with open(filename) as handle:
        for line in handle:            
            line = line.strip()[:-1]  # remove newline and drop the ')'
            ingredients, allergens = line.split(" (contains ")
            ingredients = ingredients.split(" ")
            allergens = allergens.split(", ")
            for a in allergens:
                allergen_dict.setdefault(a, [])
                if not allergen_dict[a]:
                    allergen_dict[a] = set(ingredients)
                else:
                    allergen_dict[a] = allergen_dict[a].intersection(set(ingredients))
            # Determine which ingredients cannot possibly contain any of the allergens in your list. 
            # How many times do any of those ingredients appear?
            for i in ingredients:
                ingredient_count.setdefault(i, 0)
                ingredient_count[i] += 1
            
    allergens = list(allergen_dict.keys())
    while allergens:
        for a in allergens:
            # Find allergen items that only have one possible ingredient.
            if len(allergen_dict[a]) == 1:
                # Remove that ingredient from the other allergen possible ingredients.
                allergens.remove(a)
                ingredient = list(allergen_dict[a])[0]
                for a2 in allergens:
                    allergen_dict[a2].discard(ingredient)
    
    # Remove all allergen ingredients from the count
    allergens = [list(i)[0] for i in allergen_dict.values()]
    for a in allergens:
        ingredient_count.pop(a)
    
    # Part 2
    allergens = sorted(allergen_dict.keys())
    dangerous = ""
    for a in allergens:
        dangerous += list(allergen_dict[a])[0] + ","
    dangerous = dangerous[:-1]

    return sum(ingredient_count.values()), dangerous


part1, part2 = solve("sample.txt")
assert part1 == 5
assert part2 == "mxmxvkd,sqjhc,fvjkl"

part1, part2 = solve("input.txt")
assert part1 == 2380
assert part2 == "ktpbgdn,pnpfjb,ndfb,rdhljms,xzfj,bfgcms,fkcmf,hdqkqhh"

print(f"part 1: {part1}")
print(f"part 2: {part2}")