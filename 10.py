with open("inputs/10.txt") as f:
    inp = f.read()

maze = ["%" + x + "%" for x in inp.split("\n")]
maze = ["%"*len(maze[0])] + maze + ["%"*len(maze[0])]
move_map = {
    "-": {"A" : "A", "D" : "D"},
    "|": {"W" : "W", "S" : "S"},
    "F": {"W" : "D", "A" : "S"},
    "7": {"D" : "S", "W" : "A"},
    "L": {"S" : "D", "A" : "W"},
    "J": {"D" : "W", "S" : "A"}
}

# Part 1
# Just walk through the pipe until reach start, count each step, divide by 2
# Part 2
# Too lazy to determine if loop is counter-clockwise or clockwise, just fill for one and then see if right one, if not, can count all "non-filled" ones
# Using # for enclosed symbol, . remains unenclosed
# Fill in all #s touching the inside of the loop, then later floodfill all . touching #s
# Always look to the right of the direction of travel for fill (and on 3 squares for corner symbols) 
# We can ignore | and - symbols, since any adjacent points will be filled by other means

# Starting position and direction
start_pos = [i for i in range(len(maze)) if "S" in maze[i]][0]
start_pos = [start_pos, maze[start_pos].find("S")]
if maze[start_pos[0]-1][start_pos[1]] in ["|", "F", "7"]:
    direction = "W"
elif maze[start_pos[0]+1][start_pos[1]] in ["|", "J", "L"]:
    direction = "S"
elif maze[start_pos[0]][start_pos[1]-1] in ["-", "L", "F"]:
    direction = "A"
elif maze[start_pos[0]][start_pos[1]+1] in ["-", "J", "7"]:
    direction = "D"
pos = [start_pos[0], start_pos[1]]

# Filled maze for part 2
maze_fill = [["%" if z == "%" else "." for z in x ] for x in maze]
count = 0
while True:
    count += 1
    # Compute new position
    if direction == "W":
        pos[0] -= 1
    elif direction == "S":
        pos[0] += 1
    elif direction == "A":
        pos[1] -= 1
    elif direction == "D":
        pos[1] += 1
    if pos == start_pos:
        break
    # Fill maze (for Part 2)
    maze_fill[pos[0]][pos[1]] = "O"
    simb = maze[pos[0]][pos[1]]
    indexes_to_fill = []
    if simb == "F":
        if direction == "W":
            indexes_to_fill = [[1,1]]
        else:
            indexes_to_fill = [[-1,-1],[-1,0],[0,-1]]
    elif simb == "L":
        if direction == "A":
            indexes_to_fill = [[-1,1]]
        else:
            indexes_to_fill = [[1,-1], [0,-1], [1,0]]
    elif simb == "J":
        if direction == "S":
            indexes_to_fill = [[-1,-1]]
        else:
            indexes_to_fill = [[1,1], [1,0], [0,1]]
    elif simb == "7":
        if direction == "D":
            indexes_to_fill = [[1,-1]]
        else:
            indexes_to_fill = [[-1,1], [0,1], [-1,0]]
    if len(indexes_to_fill) != 0:
        for fill in indexes_to_fill:
            fill_pos = [pos[0]+fill[0], pos[1]+fill[1]]
            if maze_fill[fill_pos[0]][fill_pos[1]] == ".":
                maze_fill[fill_pos[0]][fill_pos[1]] = "#"

    # Update direction
    direction = move_map[simb][direction]

print("Part 1:", int(count/2))

# Flood fill # chars for part 2, brute force scan all on each iteration
fill_count = 1
while fill_count > 0:
    fill_count = 0
    for i in range(len(maze_fill)):
        for j in range(len(maze_fill[i])):
            if maze_fill[i][j] == ".":
                if "#" in [maze_fill[i+1][j], maze_fill[i-1][j], maze_fill[i][j+1], maze_fill[i][j-1]]:
                    maze_fill[i][j] = "#"
                    fill_count += 1

print("Part 2:", sum([x.count("#") for x in maze_fill]))
