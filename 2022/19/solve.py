ORE = 0
CLAY = 1
OBS = 2
GEODE = 3



def get_affordable_robots(resources, costs):
    ore, clay, obs_ore, obs_clay, geode_ore, geode_obs = costs # robot costs
    robots = [0, 0, 0, 0] # ore, clay, obs, geode
    robots[ORE] = 1 if resources[ORE] >= ore else 0
    robots[CLAY] = 1 if resources[ORE] >= clay else 0
    robots[OBS] = 1 if resources[ORE] >= obs_ore and resources[CLAY] >= obs_clay else 0
    robots[GEODE] = 1 if resources[ORE] >= geode_ore and resources[OBS] >= geode_obs else 0
    return tuple(robots)


def buy_bot(blueprint, temp_resources, robots, index):
    assert isinstance(temp_resources, tuple) and isinstance(robots, tuple)
    _, ore, clay, obs_ore, obs_clay, geode_ore, geode_obs = blueprint
    resources = list(temp_resources)
    robots = list(robots)
    if index == ORE:
        resources[ORE] -= ore        
    elif index == CLAY:
        resources[ORE] -= clay
    elif index == OBS:
        resources[ORE] -= obs_ore
        resources[CLAY] -= obs_clay
    elif index == GEODE:
        resources[ORE] -= geode_ore
        resources[OBS] -= geode_obs
    robots[index] += 1
    return tuple(resources), tuple(robots)


def collect_resources(robots, temp_resources):
    assert isinstance(robots, tuple) and isinstance(temp_resources, tuple)
    resources = list(temp_resources)
    for index, robot in enumerate(robots):
        resources[index] += robot
    return robots, tuple(resources)


TIME = 32
current_max = 0
def dfs_get_most_geodes(blueprint, minute, robots, resources, not_bought, results):
    global current_max
    assert isinstance(robots, tuple) and isinstance(resources, tuple)
    if minute == 14 and robots == (1, 4, 1, 0) and resources == (3, 15, 3, 0):
        # if TIME == 15 and robots == (1, 4, 2, 0) and resources == (1, 5, 4, 0):
        print("STATE -", "robots:", robots, "res:", resources)        
    if minute > TIME:        
        current_max = max(current_max, resources[3])
        return resources[3]

    id, ore, clay, obs_ore, obs_clay, geode_ore, geode_obs = blueprint
    costs = [ore, clay, obs_ore, obs_clay, geode_ore, geode_obs]
    
    cutoff_time = 32
    remaining_time = TIME - minute
    if current_max and minute > cutoff_time:
        estimate = remaining_time * (remaining_time + 1) // 2
        future_geodes = robots[3] * (TIME - cutoff_time) + resources[3] + estimate
        if future_geodes < current_max:
            # print("PRUNING BRANCH..")
            return 0

    # get affordable robots before collecting resources
    newbots = get_affordable_robots(resources, costs)
    robots, resources = collect_resources(robots, resources)
    
    # print(f"min:{minute}, ID:{id}, bots:{robots}, newbots:{newbots}, res:{resources}, max:{current_max}")
    
    # # force buy a geode bot, ignore other options
    if newbots[GEODE] > 0:
        new_resources, tempbots = buy_bot(blueprint, resources, robots, GEODE)
        return dfs_get_most_geodes(blueprint, minute + 1, tempbots, new_resources, None, results)       
    
    # simulate saving money. not buying anything
    max_geodes = []
    temp = dfs_get_most_geodes(blueprint, minute + 1, robots, resources, newbots, results)
    if temp is not None:
        max_geodes.append(temp)

    # simulate buying any one of the affordable bots
    for index, bot in enumerate(newbots):
        if bot == 0:
            continue
        # skip bots that were not bought last round
        if not_bought and not_bought[index] > 0:
            continue
        if index == ORE and robots[ORE] >= geode_ore and robots[ORE] >= ore and robots[ORE] >= clay and robots[ORE] >= obs_ore:
            continue
        if index == CLAY and robots[CLAY] >= obs_clay:
            continue
        if index == OBS and robots[OBS] >= geode_obs:
            continue
        new_resources, tempbots = buy_bot(blueprint, resources, robots, index)
        temp = dfs_get_most_geodes(blueprint, minute + 1, tempbots, new_resources, None, results)
        if temp is not None:
            max_geodes.append(temp)
    if len(max_geodes) > 0:
        return max(max_geodes)
    return 0


blueprints = [] # array of tuples (id, ore, clay, obsidian, geode)

filename = "input.txt"
with open(filename, "r") as handle:
    for line in handle:
        line = line.strip().split()
        for i, temp in enumerate(line):
            print(i, temp)
        id = line[1][:-1]
        ore = line[6]
        clay = line[12]
        obs_ore = line[18]
        obs_clay = line[21]
        geode_ore = line[27]
        geode_obs = line[30]
        blueprint = (id, ore, clay, obs_ore, obs_clay, geode_ore, geode_obs)
        blueprint = tuple(map(int, blueprint))
        blueprints.append(blueprint)

# print(blueprints)

top_three = []
total_quality = 0
for blueprint in blueprints:
    print(blueprint)
    # resources = [0, 0, 0, 0] # ore, clay, obs, geode
    # robots = [1, 0, 0, 0] # ore, clay, obs, geode    
    results = set()    
    max_geodes = dfs_get_most_geodes(blueprint, 1, (1, 0, 0, 0), (0, 0, 0, 0), None, results)
    # part1 = max(results, key=lambda item: item[3])            
    print("max geodes:", max_geodes)
    quality = blueprint[0] * max_geodes
    total_quality += quality
    print("Quality:", quality)
    top_three.append(max_geodes)
    if blueprint[0] == 1 and filename == "sample.txt":
        if TIME == 24:
            assert quality == 9
        if TIME == 32:
            print("max geodes bp1:", max_geodes)
            assert max_geodes == 56
    if blueprint[0] == 2 and filename == "sample.txt":
        if TIME == 24:
            assert quality == 24
        if TIME == 32:
            assert max_geodes == 62
    # input("Press enter to continue..")
    if TIME == 32 and len(top_three) > 2:
        break
    # break

print(total_quality)
part2 = top_three[0] * top_three[1] * top_three[2]
print("part2", part2, top_three)
# 1487 part 1
# part2 13440 [16, 40, 21]
