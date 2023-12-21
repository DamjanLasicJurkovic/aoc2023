with open("inputs/07.txt") as f:
    inp = f.read()

from functools import cmp_to_key

# Parse card hands into lists of value integers
cards_map = dict([["23456789TJQKA"[i], i] for i in range(len("23456789TJQKA"))])
hands_bets = [[[cards_map[y] for y in x.split(" ")[0]], int(x.split(" ")[1])] for x in inp.split("\n")]

# Sort first into buckets of one category, then run sort on each of the buckets
# 0 - five of a kind, 1 - four oak, 2 - full house, 3 - three oak, 4 - two pairs, 5 - one pair, 6 - nothing
hands_buckets = [[] for i in range(7)]
for hb in hands_bets:
    n_unique = len(set(hb[0]))
    if n_unique == 1: # Five of a kind
        hands_buckets[0].append(hb)
    elif n_unique == 2: # Full house or four oak
        if (hb[0].count(hb[0][0]) in [4,1]):
            hands_buckets[1].append(hb)
        else:  
            hands_buckets[2].append(hb)
    elif n_unique == 3: # Three oak or two pairs
        if any([hb[0].count(x) == 3 for x in set(hb[0])]):
            hands_buckets[3].append(hb)
        else:
            hands_buckets[4].append(hb)
    elif n_unique == 4: # One pair
        hands_buckets[5].append(hb)
    else: # Nothing
        hands_buckets[6].append(hb)
        
# Sort within buckets
def cmp(hb1, hb2):
    for i in range(5):
        if hb1[i] > hb2[i]:
            return 1
        elif hb1[i] < hb2[i]:
            return -1
    return 0
for i in range(len(hands_buckets)):
    hands_buckets[i] = sorted(hands_buckets[i], key = cmp_to_key(cmp))

# Compute result for part 1
res = 0
rank = 0
for x in hands_buckets[::-1]:
    for y in x:
        rank += 1
        res += rank * y[1]

print("Part 1:", res)

# Part 2
j_val = "23456789TJQKA".find("J")

# Re-sort buckers, going from best to lowest
hands_buckets_2 = [[] for i in range(7)]
# 0 - cant improve anymore
hands_buckets_2[0].extend(hands_buckets[0])
# 1 - if any number of J move to 0
for hb in hands_buckets[1]:
    if hb[0].count(j_val) > 0:
        hands_buckets_2[0].append(hb)
    else:
        hands_buckets_2[1].append(hb)
# 2 - if any jokers, this goes straight to 0
for hb in hands_buckets[2]:
    if j_val in hb[0]:
        hands_buckets_2[0].append(hb)
    else:
        hands_buckets_2[2].append(hb)
# 3 - if 1 or 3 jokers, move to 1
for hb in hands_buckets[3]:
    if hb[0].count(j_val) in [1,3]:
        hands_buckets_2[1].append(hb)
    else:
        hands_buckets_2[3].append(hb)
# 4 - if two Js, got to 4oak, if 1 J, go to fullhouse
for hb in hands_buckets[4]:
    if hb[0].count(j_val) == 1:
        hands_buckets_2[2].append(hb)
    elif hb[0].count(j_val) == 2:
        hands_buckets_2[1].append(hb)
    else:
        hands_buckets_2[4].append(hb)
# 5 - if any nr of Js, go to 3oak
for hb in hands_buckets[5]:
    if hb[0].count(j_val) > 0:
        hands_buckets_2[3].append(hb)
    else:
        hands_buckets_2[5].append(hb)
# 6 - if any nr of Js, go to pair
for hb in hands_buckets[6]:
    if hb[0].count(j_val) > 0:
        hands_buckets_2[5].append(hb)
    else:
        hands_buckets_2[6].append(hb)
    
# Repeat the inner sorting, but replace all J with -1
for i in range(len(hands_buckets_2)):
    for j in range(len(hands_buckets_2[i])):
        hands_buckets_2[i][j][0] = [-1 if x == j_val else x for x in hands_buckets_2[i][j][0]]
for i in range(len(hands_buckets_2)):
    hands_buckets_2[i] = sorted(hands_buckets_2[i], key = cmp_to_key(cmp))

res = 0
rank = 0
for x in hands_buckets_2[::-1]:
    for y in x:
        rank += 1
        res += rank * y[1]

print("Part 2:", res)
