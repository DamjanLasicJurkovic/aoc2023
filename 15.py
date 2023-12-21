with open("inputs/15.txt") as f:
    inp = f.read()

inp1 = inp.split(",")

def compute_hash(str_in):
    val = 0
    for c in str_in:
        val += ord(c)
        val = val*17 % 256
    return val


# Part 1
print("Part 1:", sum([compute_hash(x) for x in inp1]))


# Part 2
buckets = [[{},[]] for i in range(256)]
for x in inp1:
    if "=" in x:
        lbl = x[0:x.find("=")]
        pos = compute_hash(lbl)
        val = int(x[x.find("=")+1::])
        if lbl not in buckets[pos][0]:
            buckets[pos][0][lbl] = len(buckets[pos][1])
            buckets[pos][1].append(val)
        else:
            buckets[pos][1][buckets[pos][0][lbl]] = val
    else: # remove
        lbl = x[0:x.find("-")]
        pos = compute_hash(lbl)
        if lbl in buckets[pos][0]:
            list_pos = buckets[pos][0].pop(lbl)
            buckets[pos][1].pop(list_pos)
            for k in buckets[pos][0].keys():
                if buckets[pos][0][k] > list_pos:
                    buckets[pos][0][k] -= 1

score = 0
for i in range(len(buckets)):
    for j in range(len(buckets[i][1])):
        score += buckets[i][1][j]*(i+1)*(j+1)
    
print("Part 2:", score)