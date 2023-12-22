with open("inputs/14.txt") as f:
    inp = f.read()

import numpy as np

inp1 = inp.split("\n")
grid = np.zeros([len(inp1), len(inp1[0])],dtype=int)
for i in range(len(inp1)):
    for j in range(len(inp1[0])):
        grid[i][j] = 2 if inp1[i][j] == "O" else 1 if inp1[i][j] == "#" else 0

def print_grid(grid):
    for i in range(grid.shape[0]):
        print("".join(["." if j == 0 else "#" if j == 1 else "O" for j in grid[i]]))
    print()

# Dir is for example [-1,0]
def move_in_dir(grid, coords, dir):
    while len(coords) > 0:
        for i in range(len(coords)):
            c = coords[i]
            if c[0] + dir[0] < 0 or c[0] + dir[0] >= grid.shape[0] or c[1] + dir[1] < 0 or c[1] + dir[1] >= grid.shape[1]:
                coords.remove(c)
                break
            if grid[c[0]+dir[0]][c[1]+dir[1]] in [1, 2]:
                coords.remove(c)
                break
            grid[c[0]][c[1]] = 0
            grid[c[0]+dir[0]][c[1]+dir[1]] = 2
            coords[i][0] += dir[0]
            coords[i][1] += dir[1]

# Coors need to be sorted with ascending [0] values
def move_up(grid):
    coord_x, coord_y = np.where(grid == 2)
    coords = [[coord_x[i], coord_y[i]]  for i in range(len(coord_x))]
    move_in_dir(grid, coords, [-1,0])

# Coors need to be sorted with descending [0] values
def move_down(grid):
    coord_x, coord_y = np.where(grid == 2)
    coords = [[coord_x[i], coord_y[i]] for i in range(len(coord_x))]
    coords.sort(key=lambda x: -x[0])
    move_in_dir(grid, coords, [1,0])

# Coors need to be sorted with ascending [1] values
def move_left(grid):
    coord_x, coord_y = np.where(grid == 2)
    coords = [[coord_x[i], coord_y[i]] for i in range(len(coord_x))]
    coords.sort(key=lambda x: x[1])
    move_in_dir(grid, coords, [0,-1])

# Coors need to be sorted with descending [1] values
def move_right(grid):
    coord_x, coord_y = np.where(grid == 2)
    coords = [[coord_x[i], coord_y[i]] for i in range(len(coord_x))]
    coords.sort(key=lambda x: -x[1])
    move_in_dir(grid, coords, [0,1])

def compute_score(grid):
    score = 0
    for i in range(grid.shape[0]):
        score += np.count_nonzero(grid[i] == 2)*(grid.shape[0] - i)
    return score

# Part 1: Simulate then compute
move_up(grid)

print("Part 1:", compute_score(grid))

# Part 2
# Simulate cycles repeatedly until start getting repeats (repeats means state is the same after N full cycles)
# Then compute closest state before 1000000000, and do the few remaining cycles
def do_cycle(grid):
    move_up(grid)
    move_left(grid)
    move_down(grid)
    move_right(grid)

# Dict with position on when a state was last reached
state_set = {}

count = 0
while True:
    count += 1
    do_cycle(grid)
    state = grid.tobytes()
    if state in state_set:
        last_rep = state_set[state]
        period = count - last_rep
        break
    else:
        state_set[state] = count

n_reps_to_do = (1000000000 - last_rep) % period

for i in range(n_reps_to_do):
    do_cycle(grid)

print("Part 2:", compute_score(grid))
