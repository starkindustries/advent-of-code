def solve():
    pass


valvemap = {} # { AA : { flow : 0, tunnels: [] }}

def parse_input(filename):    
    with open(filename, "r") as handle:
        for line in handle:
            line = line.strip().split()
            valve = line[1]
            rate = int(line[4].split("=")[1][:-1])
            print(rate)
            tunnels = [x.replace(",", "") for x in line[9:]]
            print(tunnels)
            print(valve, rate, tunnels)
            valvemap[valve] = { "flow" : rate, "tunnels" : tunnels }


def breadth_first(start, valvemap):
    edge_len = 1
    queue = [start]
    distances = {}
    distances[start] = 0

    while queue:
        valve = queue.pop(0)
        tunnels = valvemap[valve]["tunnels"]
        for tunnel in tunnels:
            if tunnel in distances:
                continue
            distances.setdefault(tunnel, 0)
            distances[tunnel] = distances[valve] + edge_len
            queue.append(tunnel)
    return distances


next_valve = "AA"
time = 1
score = 0
num_valves = len(valvemap)
# maxtime = 30

def depth_first(current, time, opened, elephant, maxtime, distances):
    assert time <= maxtime
    if time == maxtime:
        return 0

    # distances = breadth_first(current, valvemap)
    # distances = distance_lookup
    current_distances = distances[current]
    scores = []

    for _ in range(1 + elephant):
        for valve, distance in current_distances.items():
            if valve in opened:
                continue
            if valvemap[valve]["flow"] == 0:
                continue
            # Note this accounts for travel time and opening valve
            time_remaining = maxtime - time - distance
            if time_remaining <= 0:
                continue
            total_pressure = time_remaining * valvemap[valve]["flow"]
            temp_opened = opened.copy()
            temp_opened.add(valve)
            score = total_pressure + depth_first(valve, time + distance  + 1, temp_opened, elephant, maxtime, distances)
            scores.append((score, temp_opened, time_remaining, valvemap[valve]["flow"], total_pressure, valve))
    if not scores:
        # this is the case where all valves are already opened
        # therefore, no additional pressure granted
        return 0
    # for s in scores:
    #     print(f"{s[0]}, {s[1]}, {s[2]}m, rate:{s[3]}, total:{s[4]}, {s[5]}")
    # input()
    max_tuple = max(scores, key=lambda item:item[0])
    return max_tuple[0]
    
# get distances
def build_distance_lookup():
    distance_lookup = {}
    for key in valvemap:
        distances = breadth_first(key, valvemap)
        distance_lookup.setdefault(key, {})
        distance_lookup[key] = distances
    print("DISTANCES:", distance_lookup)
    # input("PRESS ENTER TO CONTINUE..")
    return distance_lookup


tunnel_pairs = set()
def build_tunnel_pairs():
    for key1 in valvemap:
        for key2 in valvemap:
            if key1 == key2:
                continue
            if valvemap[key1]["flow"] == 0 or valvemap[key2]["flow"] == 0:
                continue
            pair = tuple(sorted([key1, key2]))
            tunnel_pairs.add(pair)


def depth_first2(current1, current2, time1, time2, opened, maxtime, distance_lookup):
        
    distances1 = distance_lookup[current1]
    distances2 = distance_lookup[current2]
    scores = []

    # for pair in tunnel_pairs:
    #     valve1, valve2 = pair
    #     if valve1 in opened or valve2 in opened:
    #         continue
    #     distance1 = distances1[valve1]
    #     distance2 = distances2[valve2]        
    #     remaining1 = maxtime - time1 - distance1
    #     remaining2 = maxtime - time2 - distance2        
    #     if remaining1 <= 0 or remaining2 <= 0:
    #         continue
    #     # At this point we should have two eligible valves
    #     pressure1 = remaining1 * valvemap[valve1]["flow"]
    #     pressure2 = remaining2 * valvemap[valve2]["flow"]
    #     temp_opened = opened.copy()
    #     temp_opened.update([valve1, valve2])
    #     score = pressure1 + pressure2 + depth_first2(valve1, valve2, time1 + distance1 + 1, time2 + distance2 + 1, temp_opened, maxtime, distance_lookup)
    #     temp = (score, temp_opened, time, valvemap[valve1]["flow"], pressure1, valve1, valve2)
    #     # print("TEMP:",temp)
    #     scores.append(temp)

    for valve1, distance1 in distances1.items():
        if valve1 in opened:
            continue
        if valvemap[valve1]["flow"] == 0:
            continue
        remaining1 = maxtime - time1 - distance1
        if remaining1 <= 0:
            continue
        pressure1 = remaining1 * valvemap[valve1]["flow"]
        found_two_valves = False
        for valve2, distance2 in distances2.items():
            if valve1 == valve2: # no use opened the same valve twice
                continue
            if valve2 in opened:
                continue
            if valvemap[valve2]["flow"] == 0:
                continue            
            remaining2 = maxtime - time2 - distance2
            if remaining2 <= 0:
                continue
            found_two_valves = True
            # At this point we should have two eligible valves            
            pressure2 = remaining2 * valvemap[valve2]["flow"]
            temp_opened = opened.copy()
            temp_opened.update([valve1, valve2])
            score = pressure1 + pressure2 + \
                depth_first2(valve1, valve2, time1 + distance1 + 1, time2 + distance2 + 1, temp_opened, maxtime, distance_lookup)
            temp = (score, temp_opened, time, valvemap[valve1]["flow"], pressure1, valve1, valve2)
            # print("TEMP:",temp)
            scores.append(temp)
        if not found_two_valves:
            temp = (pressure1, opened, time, valvemap[valve1]["flow"], pressure1, valve1, valve1)
            scores.append(temp)
            # found_two_valves
            # # if we got here then only one eligible valve found
            # score = pressure1 + depth_first(valve1, time1, opened, 0, maxtime, distance_lookup)
            # temp = (score, opened, time, valvemap[valve1]["flow"], pressure1, valve1, "--")
            # scores.append(temp)
        else:
            found_two_valves = False
    
    if not scores:
        # this is the case where all valves are already opened
        # therefore, no additional pressure granted
        return 0
    # for s in scores:
    #     print(f"SCORES: {s[0]}, {s[1]}, {s[2]}m, rate:{s[3]}, total:{s[4]}, {s[5]}:{s[6]}")    
    max_tuple = max(scores, key=lambda item:item[0])    
    return max_tuple[0]


def solve():
    filename = "sample.txt"
    filename = "input.txt"
    parse_input(filename)
    
    distances = build_distance_lookup()
    result = depth_first("AA", 1, set(), 0, 30, distances)
    print("PART 1:", result)
    if filename == "sample.txt":
        assert result == 1651
    if filename == "input.txt":
        assert result == 1724

    build_tunnel_pairs()    
    result = depth_first2("AA", "AA", 1, 1, set(), 26, distances)
    print("PART 2:", result)
    if filename == "sample.txt":
        assert result == 1707
    if filename == "input.txt":
        assert result == 2283
    # Part 2: 2482 not correct; too high..
    # 2265 for part 1 input.txt WRONG..

solve()
