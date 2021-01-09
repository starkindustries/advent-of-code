
area = []
with open("input.txt", 'r') as handle:
    for line in handle:
        area.append(line.strip())

# part 1
w = len(area[0])
print(f"w: {w}")

x = 0
trees = 0
for line in area:
    if line[x % w] == "#":
        trees += 1
    x += 3
print(f"Part 1: {trees} trees")


# part 2
def countTreesAlongSlope(right, down):
    x, y = 0, 0
    trees = 0
    while y < len(area):
        if area[y][x % w] == "#":
            trees += 1
        x += right
        y += down
    return trees


slopes = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]

product = 1
for r, d in slopes:
    trees = countTreesAlongSlope(r, d)
    product *= trees
    print(f"Trees along slope[{r},{d}]: {trees}")
print(f"Part 2: {product}")
