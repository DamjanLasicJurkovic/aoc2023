inp = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""

# Parse to list of pos, velocity tuples
inp = [[eval("(" + y + ")") for y in x.split("@")] for x in inp.split("\n")]

# Part 1: ignore Z
inp1 = [[y[0:2] for y in x] for x in inp]

# Generate list of line equations for each hailstone
# y = kx + n
lines = []
for pos_vel in inp1:
    # NOTE: No 0 in any vel direction in input, so no special cases
    k = pos_vel[1][1] / pos_vel[1][0]
    n = pos_vel[0][1] - k*pos_vel[0][0]
    lines.append([k,n])

min_max = [200000000000000, 400000000000000]

# Find crossings
def cross_point(l1, l2):
    if l1[0] == l2[0]:
        return False
    x = (l1[1]-l2[1])/(l2[0]-l1[0])
    y = x*l1[0]+l1[1]
    return [x,y]

def is_in_future(c_p, p_v):
    if p_v[0][0] > c_p[0] and p_v[1][0] < 0:
        return True
    if p_v[0][0] < c_p[0] and p_v[1][0] > 0:
        return True
    return False

def is_p_in_range(p, rng):
    return p[0] >= rng[0] and p[0] <= rng[1] and p[1] >= rng[0] and p[1] <= rng[1]

count = 0
for i in range(len(lines)):
    ln1 = lines[i]
    for j in range(i+1, len(lines)):
        ln2 = lines[j]
        c_p = cross_point(ln1, ln2)
        if c_p != False:
            if is_p_in_range(c_p, min_max):
                if is_in_future(c_p, inp1[i]) and is_in_future(c_p, inp1[j]):
                    count += 1

print("Part 1:", count)

# Part 2
# Need line equations in 3D
# The solution line has to travel exactly through all of the paths
# Probably there exists just one such line
# Can compute this line, and then after compute the pos and velocity of starting point on the line



