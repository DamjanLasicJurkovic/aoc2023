with open("inputs/04.txt") as f:
    inp = f.read()

inp1 = [[[int(q) for q in z.split(" ")[1:-1]] for z in y] for y in [(x[x.find(":")+1::] + " ").replace("  ", " ").split("|") for x in inp.split("\n")]]

# Part 1
# Greedy O(N^2) search
nr_won_per_card = []
for card in inp1:
    nr_won_per_card.append(len([1 for x in card[1] if x in card[0]]))

print("Part 1:", sum([2**(x-1) for x in nr_won_per_card if x > 0]))

# Part 2
# Make a list for the amount of copies of each card
n_copies = [1 for x in nr_won_per_card]
for i in range(len(nr_won_per_card)):
    for j in range(nr_won_per_card[i]):
        n_copies[i+j+1] += n_copies[i]

print("Part 2:", sum(n_copies))
