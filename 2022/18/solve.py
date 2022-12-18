
offsets = [
    [ 1,  0,  0], 
    [-1,  0,  0],
    [ 0,  0,  1],
    [ 0,  0, -1],
    [ 0,  1,  0],
    [ 0, -1,  0],
]


def breadth_first(start, cubes, min_values, max_values):
    edge_len = 1
    queue = [start]
    distances = {}
    distances[start] = 0
    minx, miny, minz = min_values
    maxx, maxy, maxz = max_values

    while queue:
        air_position = queue.pop(0)
        x, y, z = air_position
        for offset in offsets:
            dx, dy, dz = offset
            adj_position = (x + dx, y + dy, z + dz)            
            if adj_position[0] < minx or adj_position[0] > maxx:
                # out of bounds x axis 
                continue
            if adj_position[1] < miny or adj_position[1] > maxy:
                # out of bounds x axis 
                continue
            if adj_position[2] < minz or adj_position[2] > maxz:
                # out of bounds z axis 
                continue
            if adj_position in cubes:
                # blocked by a cube
                continue
            if adj_position in distances:
                # already visited
                continue
            distances.setdefault(adj_position, 0)
            distances[adj_position] = distances[air_position] + edge_len
            queue.append(adj_position)
    return distances


def is_air_pocket(distances, min_values, max_values):
    minx, miny, minz = min_values
    maxx, maxy, maxz = max_values
    for distance in distances:
        x, y, z = distance
        if x <= minx or x >= maxx:
            return False
        if y <= miny or y >= maxy:
            return False
        if z <= minz or z >= maxz:
            return False
    return True


def find_min_max(cubes):
    xlist, ylist, zlist = [], [], []
    for cube in cubes:
        x, y, z = cube
        xlist.append(x)
        ylist.append(y)
        zlist.append(z)
    min_values = (min(xlist), min(ylist), min(zlist))
    max_values = (max(xlist), max(ylist), max(zlist))
    return (min_values, max_values)

# sample 2 has an air pocket the size of 3 cubes
filename = "input.txt"
cubes = set()
with open(filename, "r") as handle:
    for line in handle:
        if line[0] == "#":
            continue
        line = tuple(map(int, line.strip().split(",")))
        print(line)
        cubes.add(line)


min_values, max_values = find_min_max(cubes)
non_air_pockets = set()
air_pockets = set()
sides_covered = 0
# keep track of visited
# for each node, check its six sides for a touching cube
for cube in cubes:
    # check adjacent positions for neighbor cube
    x, y, z = cube    
    for offset in offsets:
        dx, dy, dz = offset
        adj_position = (x + dx, y + dy, z + dz)        
        if adj_position in cubes:
            sides_covered += 1
        elif adj_position not in air_pockets and adj_position not in non_air_pockets:
            distances = breadth_first(adj_position, cubes, min_values, max_values)
            # all of the positions in `distances` returned are connected to the adj_position
            # therefore, if ANY of the of the positions are at the edges, then the position
            # is NOT an airpacket
            # However, if NONE of the positions are at the edges, then it is an air pocket            
            print(distances)
            if is_air_pocket(distances, min_values, max_values):
                print("AIR POCKET FOUND")      
                print([key for key in distances])
                air_pockets.update([key for key in distances])                          
            else:
                print("NON AIR POCKET FOUND")
                print(distances)
                non_air_pockets.update([key for key in distances])
                
            
            # air_pockets_found += 1
            # check adjacent air pockets if trapped
for cube in cubes:
     # check adjacent positions for air pockets
    x, y, z = cube    
    for offset in offsets:
        dx, dy, dz = offset
        adj_position = (x + dx, y + dy, z + dz)        
        if adj_position in air_pockets:
            print("AIR POCKET SIDE CONFIRMED")
            sides_covered += 1
            
# calculate exposed sides
exposed = len(cubes) * 6 - sides_covered
print(exposed)
