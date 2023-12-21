with open("inputs/03.txt") as f:
    inp = f.read()

inp1 = ["." + x + "." for x in inp.split("\n")]
inp1 = ["."*(len(inp1[0]))] + inp1 + ["."*(len(inp1[0]))]

# Part 1
# Storing also adjacent gears for each number

def check_if_part_no(pos_x, pos_y, sz, grid):
    for x in [pos_x-1, pos_x+sz]:
        for y in range(pos_y-1, pos_y+2):
            if grid[y][x] != ".":
                return True

    for x in range(pos_x, pos_x+sz):
        for y in [pos_y-1, pos_y+1]:
            if grid[y][x] != ".":
                return True
            
    return False

def find_adjacent_gears(pos_x, pos_y, sz, grid):
    adj_gears = []
    for x in [pos_x-1, pos_x+sz]:
        for y in range(pos_y-1, pos_y+2):
            if grid[y][x] == "*":
                adj_gears.append([x,y])

    for x in range(pos_x, pos_x+sz):
        for y in [pos_y-1, pos_y+1]:
            if grid[y][x] == "*":
                adj_gears.append([x,y])
            
    return adj_gears

all_nums = []
for ln in inp1:
    nums = []
    num = ""
    for i in range(len(ln)):
        if ln[i].isdigit():
            num+=ln[i]
        else:
            if len(num) != 0:
                nums.append([i-len(num),num])
                num=""
    all_nums.append(nums)

part_nums_pos_adj_gears = []
for pos_y in range(len(all_nums)):
    for num in all_nums[pos_y]:
        if check_if_part_no(num[0], pos_y, len(num[1]), inp1):
            adj_gears = find_adjacent_gears(num[0], pos_y, len(num[1]), inp1)
            part_nums_pos_adj_gears.append([int(num[1]), [num[0], pos_y], adj_gears])

print("Part 1:", sum([x[0] for x in part_nums_pos_adj_gears]))

# Part 2
# Create map for each gear, which numbers are adjacent to it

adj_parts_per_gear = {}
for i in range(len(part_nums_pos_adj_gears)):
    for adj_gear in part_nums_pos_adj_gears[i][2]:
        str_gear = repr(adj_gear)
        if str_gear not in adj_parts_per_gear:
            adj_parts_per_gear[str_gear] = []
        adj_parts_per_gear[str_gear].append(i)

gear_ratios = []
for adj in adj_parts_per_gear.values():
    if len(adj) == 2:
        gear_ratios.append(part_nums_pos_adj_gears[adj[0]][0]*part_nums_pos_adj_gears[adj[1]][0])

print("Part 2:", sum(gear_ratios))
