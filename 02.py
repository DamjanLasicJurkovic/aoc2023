with open("inputs/02.txt") as f:
    inp = f.read()

inp1 = [y.replace(",",";").split("; ") for y in [x[x.find(": ")+2::] for x in inp.split("\n")]]

target = [12, 13, 14]
colors = ["red", "green", "blue"]
count = []
for i in range(len(inp1)):
    count_g = [0,0,0]
    for c in range(len(colors)):
        for s in inp1[i]:
            if colors[c] in s:
                count_g[c] = max(count_g[c], int(s[0:s.find(" ")]))
    count.append(count_g)

# Part 1
res = [True for i in range(len(inp1))]
for i in range(len(inp1)):
    for j in range(len(colors)):
        if target[j] < count[i][j]:
            res[i] = False
            break

sum_1 = 0
for i in range(len(res)):
    if res[i] is True:
        sum_1 += (i + 1)

print("Part 1:", sum_1)

# Part 2
sum_2 = 0
for i in range(len(count)):
    sum_x = 1
    for x in count[i]:
        sum_x *= x
    sum_2 += sum_x

print("Part 2:", sum_2)
