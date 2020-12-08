
n = []

filename = "input.txt"
with open(filename, 'r') as handle:
    for line in handle:
        n.append(int(line))

target = 2020
n.sort()

print(n)

for i in range(len(n) - 2):
    left = i + 1
    right = len(n) - 1
    while left < right:
        tempSum = n[i] + n[left] + n[right]        
        if tempSum == target:
            print(f"Solution: {n[i] * n[left] * n[right]}")
            exit()
        elif tempSum < target:
            left += 1
        else:
            right -= 1            
