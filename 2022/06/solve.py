from collections import deque


# Part 1
def solve(datastream, charlen):
    last_matching_index = -1
    last4 = deque([])
    marker = 0
    for char in datastream:    
        try:
            index = -1
            # match found at index
            # this index needs to get dropped off
            for i in range(len(last4)-1, -1, -1):
                if last4[i] == char:
                    index = i
                    break
            if index > last_matching_index:
                last_matching_index = index
        except Exception as e:
            print(e, char)
            
        last4.append(char)
        # print("TEMP", last4)
        marker += 1
        if len(last4) > charlen:
            last4.popleft()
            last_matching_index -= 1
        # print(char, last4, last_matching_index)
        if last_matching_index < 0 and marker >= charlen:
            # Found start-of-packet marker
            break 
    return marker


filename = "sample.txt"
with open(filename, 'r') as handle:
    for line in handle:
        datastream = line.strip()
        result = solve(datastream, 14)
        print("Part 1 sample:", result)


filename = "input.txt"
with open(filename, 'r') as handle:
    for line in handle:
        datastream = line.strip()
        result = solve(datastream, 14)
        print("Part 1 input:", result)
        break


# Part 2