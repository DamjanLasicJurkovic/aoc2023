with open("inputs/11.txt") as f:
    inp = f.read()

from copy import deepcopy
from collections import defaultdict

inp1 = inp.split("\n")
positions1 = []
for i in range(len(inp1)):
    for j in range(len(inp1[i])):
        if inp1[i][j] == "#":
            positions1.append([i,j])

# Change into coordinates, increase based on expansion (aka those that are missing from all coordinates should be expanded)
exp_amount_all = [1, 1000000-1]
for part in range(2):
    exp_amount = exp_amount_all[part]
    positions = deepcopy(positions1)

    # list of indexes of positions to increase as we pass an expansion point
    # First expansion in height direction
    inc_pos_ind = []
    inc_y = defaultdict(lambda: 0)
    for i in range(len(inp1)-1,0,-1):
        if inp1[i].count("#") == 0: # Increment all in list
            for i_pos in inc_pos_ind:
                inc_y[i_pos] += 1
        else: # Add indexes to list
            for j in range(len(inp1[i])):
                if (inp1[i][j] == "#"):
                    inc_pos_ind.append(positions.index([i,j]))
    # Then expand in width direction
    inc_pos_ind = []
    inc_x = defaultdict(lambda: 0)
    n_y = len(inp1)
    for i in range(len(inp1[0])-1,0,-1):
        if [x[i] for x in inp1].count("#") == 0: # Increment all in list
            for i_pos in inc_pos_ind:
                inc_x[i_pos] += 1
        else: # Add indexes to list
            for j in range(n_y):
                if (inp1[j][i] == "#"):
                    inc_pos_ind.append(positions.index([j,i]))

    # Inc all
    for x in inc_x.keys():
        positions[x][1] += inc_x[x]*exp_amount
    for y in inc_y.keys():
        positions[y][0] += inc_y[y]*exp_amount

    # Compute distance for each pair
    def dist(p1, p2):
        return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

    pos_tmp = deepcopy(positions)
    dists = []
    while len(pos_tmp) != 1:
        pos = pos_tmp.pop()
        for pos_to in pos_tmp:
            dists.append(dist(pos, pos_to))

    print("Part ", part + 1, ": ", sum(dists), sep="")
