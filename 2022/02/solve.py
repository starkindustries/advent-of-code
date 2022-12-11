

def solve(filename):
    # A X = rock +1
    # B Y = paper +2
    # C Z = scissors +3
    # +0 loss, +3 draw, +6 win

    points_per_move = {
        "X" : 1,
        "Y" : 2,
        "Z" : 3
    }

    move_conversion = {
        "A" : "X",
        "B" : "Y",
        "C" : "Z",    
    }

    score1 = 0

    with open(filename, 'r') as handle:
        for line in handle:        
            line = line.strip()
            (p1, p2) = line.split(" ")
            print(f"{p1} {p2}")
            score1 += points_per_move[p2]
            # convert p1's move to XYZ
            p1 = move_conversion[p1]        
            if p1 == p2:
                score1 += 3
            elif p1 == "X" and p2 == "Y":
                score1 += 6
            elif p1 == "Y" and p2 == "Z":
                score1 += 6
            elif p1 == "Z" and p2 == "X":
                score1 += 6
    print("Part 1 total score: ", score1)


    # Part 2
    # X lose, Y draw, Z win
    # A = rock +1
    # B = paper +2
    # C = scissors +3
    # +0 loss, +3 draw, +6 win
    points_per_move2 = {
        "A" : 1,
        "B" : 2,
        "C" : 3
    }

    outcome_index = {
        "X" : 0,
        "Y" : 1,
        "Z" : 2
    }

    move_to_make = {
        # Move : [loss, draw, win]
        "A" : ["C", "A", "B"],
        "B" : ["A", "B", "C"],
        "C" : ["B", "C", "A"]
    }

    outcome_points = {
        "X" : 0,
        "Y" : 3,
        "Z" : 6
    }

    score2 = 0
    with open(filename, 'r') as handle:
        for line in handle:        
            line = line.strip()
            (p1, p2) = line.split(" ")
            index = outcome_index[p2]        
            move = move_to_make[p1][index]        
            round_score = points_per_move2[move]
            round_score += outcome_points[p2]        
            print(p1, " ", index, " ", move, " ", round_score)
            score2 += round_score
    print("Part 2 total score: ", score2)
    return score1, score2


def test(path):
    part1, part2 = solve(path + "sample.txt")
    assert part1 == 15
    assert part2 == 12

    part1, part2 = solve(path + "input.txt")
    assert part1 == 11906
    assert part2 == 11186


if __name__ == "__main__":
    test("./")