with open("inputs/16.txt") as f:
    inp = f.read()

from copy import deepcopy

inp = inp.split("\n")

# Part 1
# We keep track of each path until it goes of the map or starts cycling
# We track [[position, direction], set_previous_pos_dir]
# Direction = wsad
def compute_for_starting_pos_dir(paths):
    visited_map = [[0 for i in x] for x in inp]
    already_there = set()
    while len(paths) > 0:
        for path in paths:
            visited_map[path[0]][path[1]] = 1
            if str(path) in already_there:
                paths.remove(path)
                break
            already_there.add(str(path))
            if path[2] == "a":
                if path[1] == 0:
                    paths.remove(path)
                    break
                path[1] -= 1
                next_symb = inp[path[0]][path[1]]
                if next_symb == "\\":
                    path[2] = "w"
                elif next_symb == "/":
                    path[2] = "s"
                elif next_symb == "|":
                    # Create two new paths and remove this one
                    paths.append([path[0], path[1], "w"])
                    paths.append([path[0], path[1], "s"])
                    paths.remove(path)
                    break
            elif path[2] == "d":
                if path[1] == len(inp[0]) - 1:
                    paths.remove(path)
                    break
                path[1] += 1
                next_symb = inp[path[0]][path[1]]
                if next_symb == "\\":
                    path[2] = "s"
                elif next_symb == "/":
                    path[2] = "w"
                elif next_symb == "|":
                    # Create two new paths and remove this one
                    paths.append([path[0], path[1], "w"])
                    paths.append([path[0], path[1], "s"])
                    paths.remove(path)
                    break
            elif path[2] == "w":
                if path[0] == 0:
                    paths.remove(path)
                    break
                path[0] -= 1
                next_symb = inp[path[0]][path[1]]
                if next_symb == "\\":
                    path[2] = "a"
                elif next_symb == "/":
                    path[2] = "d"
                elif next_symb == "-":
                    # Create two new paths and remove this one
                    paths.append([path[0], path[1], "a"])
                    paths.append([path[0], path[1], "d"])
                    paths.remove(path)
                    break
            elif path[2] == "s":
                if path[0] == len(inp) - 1:
                    paths.remove(path)
                    break
                path[0] += 1
                next_symb = inp[path[0]][path[1]]
                if next_symb == "\\":
                    path[2] = "d"
                elif next_symb == "/":
                    path[2] = "a"
                elif next_symb == "-":
                    # Create two new paths and remove this one
                    paths.append([path[0], path[1], "a"])
                    paths.append([path[0], path[1], "d"])
                    paths.remove(path)
                    break
    return sum([sum(x) for x in visited_map])
        
starting_pos_dir = [0,0,"d" if inp[0][0] in [".","-"] else "s"]
            
print("Part 1:", compute_for_starting_pos_dir([starting_pos_dir]))

# Part 2
# Compute for all possibilities
sym_map = {"w/" : "d", "s/" : "a", "a/" : "s", "d/" : "w",
           "w\\" : "a", "s\\" : "d", "a\\" : "w", "d\\" : "s"} 

starting_pos_dir_all = []
# Left
for i in range(len(inp)):
    symb = inp[i][0]
    if symb in ["-","."]:
        starting_pos_dir_all.append([[i, 0, "d"]])
    elif symb == "|":
        starting_pos_dir_all.append([[i, 0, "w"],[i, 0, "s"]])
    else:
        starting_pos_dir_all.append([[i, 0, sym_map["d"+symb]]])
# Right
for i in range(len(inp)):
    x = len(inp[i])-1
    symb = inp[i][x]
    if symb in ["-","."]:
        starting_pos_dir_all.append([[i, x, "a"]])
    elif symb == "|":
        starting_pos_dir_all.append([[i, x, "w"],[i, x, "s"]])
    else:
        starting_pos_dir_all.append([[i, x, sym_map["a"+symb]]])
# Top
for i in range(len(inp[0])):
    symb = inp[0][i]
    if symb in ["|","."]:
        starting_pos_dir_all.append([[0, i, "s"]])
    elif symb == "-":
        starting_pos_dir_all.append([[0, i, "a"],[0, i, "d"]])
    else:
        starting_pos_dir_all.append([[0, i, sym_map["s"+symb]]])
# Bottom
for i in range(len(inp[0])):
    y = len(inp)-1
    symb = inp[y][i]
    if symb in ["|","."]:
        starting_pos_dir_all.append([[y, i, "w"]])
    elif symb == "-":
        starting_pos_dir_all.append([[y, i, "a"],[0, i, "d"]])
    else:
        starting_pos_dir_all.append([[y, i, sym_map["w"+symb]]])

score = 0
for starting_p in starting_pos_dir_all:
    score = max(score, compute_for_starting_pos_dir(starting_p))

print("Part 2:", score)
