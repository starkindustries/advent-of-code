

def build_file_system(filename):
    print(f"Building file system for {filename}...")
    fs = {}
    with open(filename, 'r', encoding="utf8") as handle:
        # read in the first line root: "$ cd /"
        assert handle.readline().strip() == "$ cd /"

        fs["/"] = 0
        dirname = "/"
        current_dir = "/"

        for line in handle:
            line = line.strip().split()
            if line[0] == "$":
                if line[1] == "cd":
                    if line[2] == "..":
                        dirname = dirname[:-len(current_dir)-1]
                        current_dir = dirname[1:-1].split("/")[-1]
                    else:
                        current_dir = line[2]
                        dirname += line[2] + "/"
                elif line[1] == "ls":
                    continue
            elif line[0] == "dir":
                fs.setdefault(dirname+line[1]+"/", 0)
            elif line[0].isdigit():
                fs.setdefault(dirname, 0)
                fs[dirname] += int(line[0])

    # Get folder total values:
    rootsize = 0
    folder_totals = {}
    for key, value in fs.items():
        key = key[1:-1].split("/")
        path = ""
        for folder in key:
            if folder != "":
                path += folder + "/"
                folder_totals.setdefault(path, 0)
                folder_totals[path] += value
        rootsize += value
    return (folder_totals, rootsize)


def solve1(folder_totals):
    answer = 0
    for _, value in folder_totals.items():
        if value <= 100000:
            answer += value
    print("Part 1", answer)
    return answer


def solve2(folder_totals, rootsize):
    total_disk_space = 70000000
    required = 30000000
    unused = total_disk_space - rootsize
    needed = required - unused
    # print("Space unused", unused)
    # print("Space needed", needed)
    delete = []
    for _, value in folder_totals.items():
        if value >= needed:
            delete.append(value)
    answer = min(delete)
    print("Part 2", answer)
    return answer


def test(path):
    folder_totals, rootsize = build_file_system(path + "sample.txt")
    for key, value in folder_totals.items():
        print(key, value)
    assert solve1(folder_totals) == 95437
    assert solve2(folder_totals, rootsize) == 24933642

    folder_totals, rootsize = build_file_system(path + "input.txt")
    assert solve1(folder_totals) == 1334506
    assert solve2(folder_totals, rootsize) == 7421137


if __name__ == "__main__":
    test("./")
