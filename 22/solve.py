

def parse_input(filename):
    with open(filename) as handle:
        lines = [line.strip() for line in handle if line.strip() != '']
    print(lines)
    p2_index = lines.index("Player 2:")
    p1 = [int(x) for x in lines[1:p2_index]]
    p2 = [int(x) for x in lines[p2_index + 1:]]
    print(f"Player 1: {p1}")
    print(f"Player 2: {p2}")
    return p1, p2


# The game consists of a series of rounds: both players draw their 
# top card, and the player with the higher-valued card wins the 
# round. The winner keeps both cards, placing them on the bottom of 
# their own deck so that the winner's card is above the other card. 
# If this causes a player to have all of the cards, they win, and 
# the game ends.
def play_round(p1, p2):
    if not p1 or not p2:
        return False
    if p1[0] > p2[0]:
        p1.extend([p1.pop(0), p2.pop(0)])
    else:
        p2.extend([p2.pop(0), p1.pop(0)])
    return True


def solve(filename):
    p1, p2 = parse_input(filename)
    
    while play_round(p1, p2):
        continue
    
    winner = p1 if p1 else p2
    score = 0
    for i, card in enumerate(winner[::-1]):
        score += (i + 1) * card
    return score
    
assert solve("sample.txt") == 306
result = solve("input.txt")
print(f"Part 1: {result}")