with open("inputs/23.txt") as f:
    inp = f.read()

import numpy as np
import threading, sys
# Hacky way to still do recursion because didn't wanna bother rewriting
sys.setrecursionlimit(10000)
threading.stack_size(0x2000000)

inp1 = inp.split("\n")
inp1 = ["#"*len(inp1[0])] + inp1 + ["#"*len(inp1[0])]

h = len(inp1)
w = len(inp1[0])

s_pos = [1,1]
end_pos = [h-2, w-2]

visited = np.zeros((h,w), dtype=int)
visited[s_pos[0]][s_pos[1]] = 1

top_score = [0]

def can_make_move(pos, grid, move, visited, slippery):
    if slippery:
        if grid[pos[0]][pos[1]] == ">" and move != "D" or\
            grid[pos[0]][pos[1]] == "<" and move != "A" or\
            grid[pos[0]][pos[1]] == "^" and move != "W" or\
            grid[pos[0]][pos[1]] == "v" and move != "S":
            return -1 
    new_pos = [pos[0],pos[1]]
    if move == "S":
        new_pos[0] += 1
    if move == "W":
        new_pos[0] -= 1
    if move == "A":
        new_pos[1] -= 1
    if move == "D":
        new_pos[1] += 1
    if grid[new_pos[0]][new_pos[1]] == "#":
        return -1
    if visited[new_pos[0]][new_pos[1]] == 1:
        return -1
    return new_pos

def try_all_moves(pos, grid, visited, top_score, end_pos, slippery=True):
    if pos == end_pos:
        sc = np.sum(np.sum(visited))+1
        if sc > top_score[0]:
            print("New best:", sc)
            top_score[0] = sc
        return
    visited[pos[0]][pos[1]] = 1
    for move in "SDAW":
        new_pos = can_make_move(pos, grid, move, visited, slippery)
        if new_pos != -1:
            try_all_moves(new_pos, grid, visited, top_score, end_pos, slippery)
    visited[pos[0]][pos[1]] = 0


class callable:
    def __init__(self, s_pos, inp1, visited, top_score, end_pos, part_n):
        self.s_pos = s_pos
        self.inp1 = inp1
        self.visited = visited
        self.top_score = top_score
        self.end_pos = end_pos
        self.part_n = part_n

    def __call__(self):
        try_all_moves(self.s_pos, self.inp1, self.visited, self.top_score, self.end_pos, self.part_n==1)
        print("Part ", self.part_n, ": ", self.top_score[0]-1, sep="")

# Part 1
t = threading.Thread(target=callable(s_pos, inp1, visited, top_score, end_pos, 1))
t.start()
t.join()

# Part 2
t = threading.Thread(target=callable(s_pos, inp1, visited, top_score, end_pos, 2))
t.start()
t.join()
