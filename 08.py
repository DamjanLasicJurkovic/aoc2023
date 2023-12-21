with open("inputs/08.txt") as f:
    inp = f.read()

import math, copy

# Make into array and indexes, steps are 0 and 1
steps = [1 if x == "R" else 0 for x in inp.split("\n\n")[0]]
points = inp.split("\n\n")[1].split("\n")
points_mapping = dict([[points[i][0:points[i].find(" =")], i] for i in range(len(points))])
points = [[points_mapping[x[7:10]], points_mapping[x[12:15]]] for x in points]

# Part 1
# Just simulate walking through
count = 0
i = points_mapping["AAA"]
i_end = points_mapping["ZZZ"]
while i != i_end:
    for step in steps:
        i = points[i][step]
        count += 1
        if i == i_end:
            break

print("Part 1:", count)

# Part 2
# Find repeat intervals for Z ending nodes for all points
i_start = [points_mapping[x] for x in points_mapping.keys() if x[2] == "A"]
end_set = set([points_mapping[x] for x in points_mapping.keys() if x[2] == "Z"])
count = [0 for x in i_start]
rep = [0 for x in i_start]
last_rep = [0 for x in i_start]
done = [False for x in i_start]
total_count = 0
while sum(done) != len(i_start):
    for step in steps:
        total_count += 1
        for i in range(len(i_start)):
            if not done[i]:
                i_start[i] = points[i_start[i]][step]
                count[i] += 1
                if i_start[i] in end_set:
                    if (count[i] == rep[i]):
                        done[i] = True
                    else:
                        rep[i] = count[i]
                        last_rep[i] = total_count
                    count[i] = 0


# Based on last_rep and rep, have to find total number of steps = X
# X = last_rep[i] + rep[i]*N[i], where N is an arbitrary positive integer for all points
# Combine pairs of periods and starting point to common starting points and periods, eliminating one of them
# Repeat until only one pair remains
starts_periods = [[last_rep[i], rep[i]] for i in range(len(rep))]

def find_common_start_period(sp_1, sp_2):
    # Find first step nr where they are the same value
    # Just keep numerically incrementing
    while sp_1[0] != sp_2[0]:
        abs_diff = abs(sp_1[0] - sp_2[0])
        if sp_1[0] < sp_2[0]:
            if (abs_diff % sp_1[1] == 0):
                sp_1[0] += abs_diff
            else:
                sp_1[0] += sp_1[1]*(int(abs_diff/sp_1[1])+1)
        else:
            if (abs_diff % sp_2[1] == 0):
                sp_2[0] += abs_diff
            else:
                sp_2[0] += sp_2[1]*(int(abs_diff/sp_2[1])+1)
    # Compute least common multiple as new common period
    return sp_1[0], math.lcm(sp_1[1], sp_2[1])

while len(starts_periods) > 1:
    comm_start, comm_per = find_common_start_period(starts_periods[-1], starts_periods[-2])
    starts_periods.pop()
    starts_periods[-1] = [comm_start, comm_per]

print("Part 2:", starts_periods[0][0])
