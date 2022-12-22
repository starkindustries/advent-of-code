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


def buy_bot(blueprint, resources, index):
    _, ore, clay, obs_ore, obs_clay, geode_ore, geode_obs = blueprint
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
    return tuple(resources)


# def breadth_first(start, valvemap):
#     edge_len = 1
#     queue = [start]
#     distances = {}
#     distances[start] = 0

#     while queue:
#         valve = queue.pop(0)
#         tunnels = valvemap[valve]["tunnels"]
#         for tunnel in tunnels:
#             if tunnel in distances:
#                 continue
#             distances.setdefault(tunnel, 0)
#             distances[tunnel] = distances[valve] + edge_len
#             queue.append(tunnel)
#     return distances


# def bfs_get_most_geodes(blueprint):
#     id, ore, clay, obs_ore, obs_clay, geode_ore, geode_obs = blueprint
#     costs = [ore, clay, obs_ore, obs_clay, geode_ore, geode_obs]
#     queue = [((1, 0, 0, 0), (0, 0, 0, 0), 1, (0, 0, 0, 0))] # bots, resources, min, bots not bought
#     result_resources = set()

#     while queue:
#         robots, resources, minute, bots_not_built = queue.pop(0)
#         if minute > TIME:
#             result_resources.add(resources[3])
#             continue
#         # get affordable robots before collecting resources
#         newbots = get_affordable_robots(resources, costs)
#         # collect resources
#         for index, robot in enumerate(robots):
#             resources = list(resources)
#             resources[index] += robot
#             resources = tuple(resources)
        
#         queue.append((tuple(tempbots), new_resources, minute + 1, (0, 0, 0, 0)))

#         # force buy a geode bot
#         if newbots[GEODE] > 0:
#             tempbots = list(robots)
#             tempbots[index] += bot
#             new_resources = buy_bot(blueprint, resources, index)
#             queue.append((tuple(tempbots), new_resources, minute + 1, (0, 0, 0, 0)))
#             continue

#         for type, bot in enumerate(newbots):
#             if bot <= 0:
#                 continue
#             if bot > 0 and robots[type] == 0:
#                 tempbots = list(robots)
#                 tempbots[index] += bot
#                 new_resources = buy_bot(blueprint, resources, index)
#                 queue.append((tuple(tempbots), new_resources, minute + 1, (0, 0, 0, 0)))
#                 break            
#             tempbots = list(robots)
#             tempbots[index] += bot
#             new_resources = buy_bot(blueprint, resources, index)
#             queue.append((tuple(tempbots), new_resources, minute + 1, (0, 0, 0, 0)))
        
#         # # DEBUG
#         # if minute == 5:
#         #     print("DEBUG")
#         # # force buying a clay bot if none available
#         # if robots[CLAY] < 1 and newbots[CLAY] > 0:
#         #     pass
#         # # force buying an obs bot if none available
#         # elif robots[OBS] < 1 and newbots[OBS] > 0:
#         #     pass
#         # # force buying a geode always
#         # elif newbots[GEODE] > 0:
#         #     pass
#         # else:
#         #     # simulate not buying any bots with exceptions
#         #     # temp = list(newbots)
#         #     # for i in range(len(newbots)):
#         #     #     temp[i] += bots_not_built[i]
#         #     # temp = tuple(temp)
#         #     queue.append((robots, resources, minute + 1, newbots))
#         # # simulate buying any one of the affordable bots
#         # # note if a robot buying opportunity was skipped, 
#         # # cannot buy that bot in the future bc that is just wasted 
#         # # resources
#         # newbots = list(newbots)
#         # for i in range(len(newbots)):
#         #     newbots[i] -= bots_not_built[i]
#         # newbots = tuple(newbots)
#         # for index, bot in enumerate(newbots):
#         #     if bot <= 0:
#         #         continue
#         #     tempbots = list(robots)
#         #     tempbots[index] += bot
#         #     new_resources = buy_bot(blueprint, resources, index)
#         #     queue.append((tuple(tempbots), new_resources, minute + 1, (0, 0, 0, 0)))
#         # print(f"min:{minute}, ID:{id}, bots:{robots}, newbots:{newbots}, res:{resources}")
#     return result_resources

TIME = 15
def dfs_get_most_geodes(blueprint, minute, robots, resources, results):
    assert isinstance(robots, tuple) and isinstance(resources, tuple)
    if minute == 14 and robots == (1, 4, 1, 0) and resources == (3, 15, 3, 0):
        # if TIME == 15 and robots == (1, 4, 2, 0) and resources == (1, 5, 4, 0):
        print("STATE -", "robots:", robots, "res:", resources)        
    if minute > TIME:        
        results.add(tuple(resources))
        return
    _, ore, clay, obs_ore, obs_clay, geode_ore, geode_obs = blueprint
    costs = [ore, clay, obs_ore, obs_clay, geode_ore, geode_obs]
    
    # resources = [0, 0, 0, 0] # ore, clay, obs, geode
    # robots = [1, 0, 0, 0] # ore, clay, obs, geode
    # new_bots = [0, 0, 0, 0]

    # get affordable robots before collecting resources
    newbots = get_affordable_robots(resources, costs)
    # collect resources
    for index, robot in enumerate(robots):
        resources = list(resources)
        resources[index] += robot
    # print(f"min:{minute}, ID:{id}, bots:{robots}, newbots:{newbots}, res:{resources}")
    
    # force buy a geode bot, ignore other options
    if newbots[GEODE] > 0:
        tempbots = list(robots)
        tempbots[GEODE] += 1
        new_resources = buy_bot(blueprint, resources, GEODE)
        dfs_get_most_geodes(blueprint, minute + 1, tuple(tempbots), new_resources, results)    
        return
    # force buy a clay or obs bot if none owned:
    if newbots[CLAY] > 0 and robots[CLAY] == 0:
        tempbots = list(robots)
        tempbots[CLAY] += 1
        new_resources = buy_bot(blueprint, resources, CLAY)
        dfs_get_most_geodes(blueprint, minute + 1, tuple(tempbots), new_resources, results)    
        return
    # force buy a clay or obs bot if none owned:
    if newbots[OBS] > 0 and robots[OBS] == 0:
        tempbots = list(robots)
        tempbots[OBS] += 1
        new_resources = buy_bot(blueprint, resources, OBS)
        dfs_get_most_geodes(blueprint, minute + 1, tuple(tempbots), new_resources, results)    
        return
    
    # simulate saving money. not buying anything
    dfs_get_most_geodes(blueprint, minute + 1, robots, tuple(resources), results)
    
    # simulate buying any one of the affordable bots
    for index, bot in enumerate(newbots):
        tempbots = list(robots)
        if bot == 0:
            continue
        tempbots[index] += 1
        new_resources = buy_bot(blueprint, resources, index)
        dfs_get_most_geodes(blueprint, minute + 1, tuple(tempbots), new_resources, results)    
    return


blueprints = [] # array of tuples (id, ore, clay, obsidian, geode)

filename = "sample.txt"
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

print(blueprints)


for blueprint in blueprints:
    # resources = [0, 0, 0, 0] # ore, clay, obs, geode
    # robots = [1, 0, 0, 0] # ore, clay, obs, geode    
    results = set()
    # results = bfs_get_most_geodes(blueprint)
    dfs_get_most_geodes(blueprint, 1, (1, 0, 0, 0), (0, 0, 0, 0), results)
    part1 = max(results, key=lambda item: item[3])
    print("ANSWER:", part1)
    # input("Press enter to continue..")
    break

