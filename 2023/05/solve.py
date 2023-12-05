# seed-to-soil map:
#             seeds     soil
# 50 98 2  => 098-099 : 050-051
# 52 50 48 => 050-097 : 052-099
#             000-049 : 000-049 (implied range)
#             100-inf : 100-inf (implied range)

# soil-to-fertilizer map:
#             soil      fertilizer
# 0 15 37  => 015-051 : 000-036        
# 37 52 2  => 052-053 : 037-038
# 39 0 15  => 000-014 : 039-053

# fertilizer-to-water map:
#            
# 49 53 8  => 053-060 : 049-056
# 0 11 42  => 011-052 : 000-041
# 42 0 7   => 000-006 : 042-048
# 57 7 4   => 007-010 : 057-060

# water-to-light map:
# 88 18 7  => 018-024 : 088-094
# 18 25 70 => 025-094 : 018-087

# light-to-temperature map:
# 45 77 23 => 77-99 : 45-67, -32
# 81 45 19 => 45-63 : 81-99, +36
# 68 64 13 => 64-76 : 68-80,  +4

#
# seed ranges: 79 14 55 13 => ranges: 079-092, 055-067
# seeds to soil:                      081-094, 057-069
# soil to fertilizer:                 081-094, 057-069      
# fertilizer to water:                081-094, 053-056, 061-069
# water to light:                     074-087, 046-049, 054-062 correct
# light to temp:                      078-080, 045-055, 082-085, 090-098 
#                                     ^        ^        ^        ^

def solve(filename):
    seed_maps = []
    temp_map = []

    with open(filename, "r", encoding="utf8") as handle:
        lines = handle.readlines()
    
    for line in lines:
        line = line.strip()
        if "seeds" in line:
            temp = line.split(":")
            seeds = list(map(int, temp[1].strip().split(" ")))
            continue
        if line == "":
            continue
        if "map" in line:
            if len(temp_map) > 0:
                seed_maps.append(temp_map)
            temp_map = []
            continue
        data = list(map(int, line.split(" ")))
        temp_map.append(data)
        print(data)
    seed_maps.append(temp_map)
    print(seed_maps)

    # get location, part1
    results = []
    for seed in seeds:
        temp_res = [seed]
        for s_map in seed_maps:
            for data in s_map:
                dst, src, length = data
                if src <= seed <= (src + length - 1):
                    # found a matching range
                    seed = seed - src + dst
                    break
            temp_res.append(seed)
            print(seed, temp_res)
        results.append(temp_res)
    locations = [x[-1] for x in results]
    part1 = min(locations)

    # part 2
    seed_ranges = []
    seeds_copy = seeds.copy()
    while seeds_copy:
        start = seeds_copy[0]
        length = seeds_copy[1]
        seed_ranges.append([start, start+length-1])
        seeds_copy.pop(0)
        seeds_copy.pop(0)
    print(seed_ranges)
    
    ranges = set(map(tuple, seed_ranges.copy()))
    for smap in seed_maps:
        new_ranges = set()
        while ranges:
            left, right = ranges.pop()
            found_left, found_right = False, False
            for dst, src, length in smap:
                src_end = src + length - 1
                lir = src <= left  <= src_end # left-in-range
                rir = src <= right <= src_end # right-in-range
                print(f"{src}-{src+length-1} : {dst}-{dst+length-1}")
                print(f"{src} <= {left} {lir},{right} {rir} <= {src_end}")
                if lir and rir:
                    new_ranges.add((left-src+dst, right-src+dst))
                    found_left = True
                    found_right = True
                elif lir:
                    new_ranges.add((left-src+dst, dst+length-1))
                    ranges.add((src+length, right))
                    found_left = True
                elif rir:
                    new_ranges.add((dst, right-src+dst))
                    ranges.add((left, src-1))
                    found_right = True
            if not found_left and not found_right:
                new_ranges.add((left, right))
        print(new_ranges)
        # breakpoint()
        ranges = new_ranges
    print(ranges)
    low_locations = [x[0] for x in ranges]
    part2 = min(low_locations)

    return part1, part2

def test(path):
    part1, part2 = solve(path + "sample.txt")
    print(part1, part2)
    assert part1 == 35
    assert part2 == 46
    print("Test successful")

    res = solve(path + "input.txt")
    print(res)

if __name__ == "__main__":
    test("./")
