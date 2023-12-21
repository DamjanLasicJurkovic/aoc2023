with open("inputs/09.txt") as f:
    inp = f.read()

lists = [[int(y) for y in x.split(" ")] for x in inp.split("\n")]

predicted = [0, 0]
for l in lists:
    la = [l]
    while set(la[-1]) != {0}:
        la.append([])
        for i in range(1, len(la[-2])):
            la[-1].append(la[-2][i] - la[-2][i-1])
    # Part 1: Sum all last numbers in lists
    predicted[0] += sum([x[-1] for x in la])
    # Part 2: Compute as in the instructions
    pred2 = 0
    for x in la[-2::-1]:
        pred2 = x[0] - pred2
    predicted[1] += pred2

print("Part 1:", predicted[0])
print("Part 2:", predicted[1])
