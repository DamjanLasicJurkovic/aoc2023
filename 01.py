with open("inputs/01.txt") as f:
    inp = f.read()

# Part 1
print("Part 1:", sum([int(y[0]+y[-1]) for y in [[x[0],x[0]] if len(x)==1 else x for x in [[b for b in a if b.isdigit()] for a in inp.split("\n")]]]))

# Part 2
inp = inp.split("\n")
digs = ['zero','one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
repl = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']
indexes_vals = [[-1,-1,-1,-1] for i in range(len(inp))]
for n in range(len(inp)):
    for i in range(10):
        for s in [digs[i], repl[i]]:
            index = inp[n].find(s)
            if (index != -1):
                for offset in [0,1]:
                    if (indexes_vals[n][2+offset] == -1):
                        indexes_vals[n][2+offset] = str(i)
                        indexes_vals[n][0+offset] = index
                    else:
                        if offset == 0 and (indexes_vals[n][0+offset] > index) or offset == 1 and (indexes_vals[n][0+offset] < index):
                            indexes_vals[n][2+offset] = str(i)
                            indexes_vals[n][0+offset] = index
            index = inp[n].rfind(s)
            if (index != -1):
                for offset in [0,1]:
                    if (indexes_vals[n][2+offset] == -1):
                        indexes_vals[n][2+offset] = str(i)
                        indexes_vals[n][0+offset] = index
                    else:
                        if offset == 0 and (indexes_vals[n][0+offset] > index) or offset == 1 and (indexes_vals[n][0+offset] < index):
                            indexes_vals[n][2+offset] = str(i)
                            indexes_vals[n][0+offset] = index

print("Part 2:", sum([int(x[2]+x[3]) for x in indexes_vals]))
