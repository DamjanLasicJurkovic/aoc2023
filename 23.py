inp="""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

import numpy as np

inp1 = inp.split("\n")
inp1 = ["#"*len(inp1[0])] + inp1 + ["#"*len(inp1[0])]

[print(x) for x in inp1]

h = len(inp1)
w = len(inp1[0])

s_pos = [1,1]
end_pos = [h-2, w-2]

visited = np.zeros((h,w), dtype=int)
visited[s_pos[0]][s_pos[1]] = 1

top_score = [0]

def can_make_move(pos, grid, direction, visited):
    # TODO: Implement

    

def try_all_moves(pos, grid, visited, top_score, end_pos):
    if pos == end_pos:
        sc = np.sum(np.sum(visited))+1
        if sc > top_score[0]:
            print("New best:", sc)
            top_score[0] = sc
        return
    visited[pos[0]][pos[1]] = 1
    for move in "SDAW":
        if can_make_move(pos, grid, move, visited):
            new_pos = [pos[0]][pos[1]]
            if move == "S":
                new_pos[0] += 1
            if move == "W":
                new_pos[0] -= 1
            if move == "A":
                new_pos[1] -= 1
            if move == "D":
                new_pos[1] += 1
            try_all_moves(new_pos, grid, visited, top_score, end_pos)
    visited[pos[0]][pos[1]] = 0

# Part 1
try_all_moves(s_pos, inp1, visited, top_score, end_pos)
print("Part 1:", top_score[0])
