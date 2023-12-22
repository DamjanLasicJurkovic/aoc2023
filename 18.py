with open("inputs/18.txt") as f:
    inp = f.read()

from copy import deepcopy
import numpy as np

# Shoelace formula to compute the area of a simple polynom
def compute_area(pts):
    area = 0.0
    for i in range(len(pts)-1):
        p_1 = pts[i]
        p_2 = pts[i+1]
        a = 0.5*(p_1[0] + p_2[0])*(p_1[1] - p_2[1])
        area += a
    return area

def comp(instr):
    # Generate list of points that form the excavator path
    pos_list = [[0,0]]
    for x in instr:
        new_pos = deepcopy(pos_list[-1])
        if x[0] in ["U","D"]:
            new_pos[0] += x[1] if x[0] == "D" else -x[1]
        if x[0] in ["L","R"]:
            new_pos[1] += x[1] if x[0] == "R" else -x[1]
        pos_list.append(new_pos)

    # Normalize to 0
    min_x = min([x[1] for x in pos_list])
    min_y = min([x[0] for x in pos_list])
    for x in pos_list:
        x[0] -= min_y
        x[1] -= min_x

    return int(compute_area(pos_list) + sum([x[1] for x in inp1])/2+1)

# Part 1

inp1 = [[x.split(" ")[0], int(x.split(" ")[1])] for x in inp.split("\n")]

print("Part 1:", comp(inp1))

# Part 2

inp1 = [x.split(" ")[2][2:-1] for x in inp.split("\n")]
move_map = {"0": "R", "1": "D", "2": "L", "3": "U"}
inp1 = [[move_map[x[-1]], int(x[0:-1],16)] for x in inp1]

print("Part 2:", comp(inp1))
