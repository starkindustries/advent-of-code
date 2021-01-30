

def parse_input(filename):
    with open(filename) as handle:
        lines = [line.strip() for line in handle if line.strip() != '']
    p2_index = lines.index('Player 2:')
    p1 = [int(x) for x in lines[1:p2_index]]
    p2 = [int(x) for x in lines[p2_index + 1:]]
    return p1, p2


# The game consists of a series of rounds: both players draw their 
# top card, and the player with the higher-valued card wins the 
# round. The winner keeps both cards, placing them on the bottom of 
# their own deck so that the winner's card is above the other card. 
# If this causes a player to have all of the cards, they win, and 
# the game ends.
def play_combat(p1, p2):
    if not p1 or not p2:
        return False
    winner = p1 if p1[0] > p2[0] else p2
    loser = p1 if p1[0] < p2[0] else p2
    combat_helper(winner, loser)    
    return True


def combat_helper(winner, loser):
    winner.extend([winner.pop(0), loser.pop(0)])

# ***************************
# Recursive Combat Changes
# ***************************
# 1) Before either player deals a card, if there was a previous 
# round in this game that had exactly the same cards in the same 
# order in the same players' decks, the game instantly ends in a win 
# for player 1. Previous rounds from other games are not considered. 
# (This prevents infinite games of Recursive Combat, which everyone 
# agrees is a bad idea.)

# 2) Otherwise, this round's cards must be in a new configuration; 
# the players begin the round by each drawing the top card of their 
# deck as normal.

# 3) If both players have at least as many cards remaining in their 
# deck as the value of the card they just drew, the winner of the 
# round is determined by playing a new game of Recursive Combat 
# (see below).

# 4) Otherwise, at least one player must not have enough cards left 
# in their deck to recurse; the winner of the round is the player 
# with the higher-value card.
def play_recursive_combat(p1, p2, previous_rounds=set()):
    assert p1 and p2
    
    # Change #1: check for an infinite loop
    round_hash = tuple(p1) + ('||',) + tuple(p2)
    if round_hash in previous_rounds:
        return True  # player 1 instantly wins
    previous_rounds.add(round_hash)

    # Change #2: draw top card
    t1, t2 = p1[0], p2[0]
    
    # Change #3: check if both players have enough cards >= to the card drawn
    if t1 <= (len(p1) - 1) and t2 <= (len(p2) - 1):
        # play new game of recursive combat
        p1_subgame, p2_subgame = p1[1:t1+1], p2[1:t2+1]
        player1_wins = False
        subgame_previous = set()
        while p1_subgame and p2_subgame:
            if play_recursive_combat(p1_subgame, p2_subgame, subgame_previous):
                player1_wins = True
                break
        if player1_wins:
            combat_helper(p1, p2)
        else:
            combat_helper(p1 if p1_subgame else p2, p1 if not p1_subgame else p2)
    else:
        # Change #4: one player does not have enough cards
        # Therefore, winner is the player with higher-value card
        combat_helper(p1 if t1 > t2 else p2, p1 if t1 < t2 else p2)

    return False  # player 1 did NOT instantly win


def calculate_score(winner):
    score = 0
    for i, card in enumerate(winner[::-1]):
        score += (i + 1) * card
    return score

def solve(filename):
    # Part 1
    p1, p2 = parse_input(filename)        
    while play_combat(p1, p2):
        continue    
    score1 = calculate_score(p1 if p1 else p2)

    # Part 2
    p1, p2 = parse_input(filename)
    previous = set()
    while p1 and p2:
        play_recursive_combat(p1, p2, previous)
    score2 = calculate_score(p1 if p1 else p2)

    return score1, score2
    
score1, score2 = solve('sample.txt')
assert score1 == 306
assert score2 == 291

score1, score2 = solve('input.txt') 
assert score1 == 30780
assert score2 == 36621

print(f'Part 1: {score1}')
print(f'Part 2: {score2}')