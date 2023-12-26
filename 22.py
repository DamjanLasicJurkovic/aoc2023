inp="""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

import numpy as np
from collections import defaultdict

inp1 = [[eval(y) for y in x.split("~")] for x in inp.split("\n")]
inp1 = [(i, inp1[i][0], inp1[i][1]) for i in range(len(inp1))]

# Part 1
# Have a height map, a topmost index map, and dicts for supported by and supporting

# Find max x and y to generate height map and top map
max_x = max([max([br[1][0], br[2][0]]) for br in inp1])
max_y = max([max([br[1][1], br[2][1]]) for br in inp1])

heightmap = np.zeros([max_x+1,max_y+1], dtype=int)
topmap = np.ones([max_x+1,max_y+1], dtype=int)*-1 # -1 represents the floor
is_supporting = [[] for br in inp1]
is_supported_by = [[] for br in inp1]

# Sort input bricks by lowest z coordinate, and just add them in that order to heightmaps etc
def comp_key(br):
    return min(br[1][2], br[2][2])

inp1.sort(key=comp_key)

def gen_xy_pts(br):
    if br[1][2] != br[2][2]:
        return [[br[1][0],br[1][1]]], abs(br[1][2] - br[2][2])+1
    elif br[1][1] != br[2][1]:
        pts = [[br[1][0], i] for i in range(min(br[1][1], br[2][1]), max(br[1][1], br[2][1]) + 1)]
        return pts, 1
    elif br[1][0] != br[2][0]:
        pts = [[i, br[1][1]] for i in range(min(br[1][0], br[2][0]), max(br[1][0], br[2][0]) + 1)]
        return pts, 1
    else:
        return [[br[1][0],br[1][1]]], 1
        
def get_new_base_z_at_pts(xy_pts, hmap):
    all_zs = [hmap[p[0]][p[1]] for p in xy_pts]
    return max(all_zs)

def descend_brick(br, hmap, tmap, is_supp, supp_by):
    xy_pts, z_height = gen_xy_pts(br)
    
    new_z = get_new_base_z_at_pts(xy_pts, hmap)

    # Not supp by etc
    supp_by_indexes = set()
    for pt in xy_pts:
        if hmap[pt[0]][pt[1]] == new_z:
            val_under = tmap[pt[0]][pt[1]]
            if val_under != -1:
                supp_by_indexes.add(val_under) 
    for supp in supp_by_indexes:
        is_supp[supp].append(br[0])
        supp_by[br[0]].append(supp)

    # Add to hmap, tmap
    for pt in xy_pts:
        hmap[pt[0]][pt[1]] = new_z + z_height
        tmap[pt[0]][pt[1]] = br[0]
    
for br in inp1:
    descend_brick(br, heightmap, topmap, is_supporting, is_supported_by)

# See which are supporting any bricks that are supported by any other bricks
count = 0
for is_supp in is_supporting:
    if len(is_supp) == 0:
        count += 1
    else:
        all_ok = True
        for supp in is_supp:
            if len(is_supported_by[supp]) == 1:
                all_ok = False
                break
        if all_ok:
            count += 1

print("Part 1:", count)

# Part 2
# For each brick, compute how many would fail in chain reaction if it were to be disintegrated
# Go through and simulate for all, making deep copies of the dicts for each
from copy import deepcopy
nr_that_would_fail = []

def rm(br_index, is_supp, supp_by, n):
    n[0] += 1
    for br in is_supp[br_index]:
        supp_by[br].remove(br_index)
        if len(supp_by[br]) == 0:
            rm(br, is_supp, supp_by, n)
    
def determine_n_to_fail(br_index, is_supp, supp_by):
    n_fail = [-1]
    rm(br_index, is_supp, supp_by, n_fail)
    return n_fail[0]

for i in range(len(inp1)):
    is_supp = deepcopy(is_supporting)
    supp_by = deepcopy(is_supported_by)
    nr_that_would_fail.append(determine_n_to_fail(i, is_supp, supp_by))

print("Part 2:", sum(nr_that_would_fail))
