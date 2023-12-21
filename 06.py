with open("inputs/06.txt") as f:
    inp = f.read()

times, dists = [[z.strip() for z in x.split()[1::]] for x in inp.split("\n")]
times, dists = [[[int(y) for y in x] if i == 0 else [int("".join(x))] for i in [0, 1]] for x in [times, dists]]

# Both parts, greedy algorithm (sorry, CPU)
# Dist = (t_end - hold_time)*hold_time
for part_i in range(2):
    n_ways_prod = 1
    for i in range(len(times[part_i])):
        t_end = times[part_i][i]
        d = dists[part_i][i]
        n_ways = 0
        for hold_t in range(1, t_end):
            if (t_end - hold_t)*hold_t > d:
                n_ways += 1
        n_ways_prod *= n_ways
            
    print("Part ", part_i + 1, ": ", n_ways_prod, sep="")
