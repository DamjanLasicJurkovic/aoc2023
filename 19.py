with open("inputs/19.txt") as f:
    inp = f.read()

from copy import deepcopy

parts = inp.split("\n\n")[1].split("\n")
parts = [eval(x.replace("x=","").replace("m=","").replace("a=","").replace("s=","").replace("{","[").replace("}","]")) for x in parts]

workflows = inp.split("\n\n")[0].split("\n")
workflows = [x.split("{") for x in workflows]
str_names = [x[0] for x in workflows]
workflows = [x[1][0:-1].split(",") for x in workflows]
def map_name_to_index(name, str_names):
    if name in ["A","R"]:
        return name
    return str_names.index(name)

for i in range(len(workflows)):
    for j in range(len(workflows[i])):
        s = workflows[i][j]
        if ":" not in s:
            workflows[i][j] = [map_name_to_index(s, str_names)]
        else:
            workflows[i][j] = ["xmas".index(s[0]), s[1], int(s[2:s.find(":")]), map_name_to_index(s[s.find(":")+1::], str_names)]

# Part 1
# Send each part through the workflows
starting_wf_index = str_names.index("in")
accepted = []
for x in parts:
    wf = workflows[starting_wf_index]
    keep = True
    while keep:
        for check in wf:
            if len(check) == 1:
                if check == ["A"]:
                    accepted.append(x)
                    keep = False
                elif check == ["R"]:
                    keep = False
                else:
                    wf = workflows[check[0]]
                break
            else: # Is a check
                check_yes = False
                if check[1] == ">":
                    check_yes = x[check[0]] > check[2]
                elif check[1] == "<":
                    check_yes = x[check[0]] < check[2]
                if check_yes:
                    if check[3] == "A":
                        accepted.append(x)
                        keep = False
                    elif check[3] == "R":
                        keep = False
                    else:
                        wf = workflows[check[3]]
                    break

print("Part 1:", sum([sum(x) for x in accepted]))

# Part 2
# Start from in with full range, keep adjusting and generating new ranges as they split

# Returns new list of ranges
def handle_wf_for_range(rng, workflows, accepted):
    wf = workflows[rng[4]]
    new_ranges = []
    for check in wf:
        if len(check) == 1:
            if check == ["A"]:
                accepted.append(rng)
            elif check == ["R"]:
                pass
            else:
                rng[4] = check[0]
                new_ranges.append(rng)
            return new_ranges
        else:
            # Split the range in two, or keep one
            # For each, accept, delete, or forward to another workflow
            mn = rng[check[0]][0]
            mx = rng[check[0]][1]
            range_to_mv = 0
            if check[1] == ">":
                if mn >= check[2]: # means whole range gets transferred
                    if check[3] == "A":
                        accepted.append(rng)
                        return new_ranges
                    elif check[3] == "R": # discard range
                        return new_ranges
                    else:
                        rng[4] = check[3]
                        new_ranges.append(rng)
                        return new_ranges
                elif mx > check[2]: # part of the range gets transfered
                    nw = deepcopy(rng)
                    rng[check[0]][1] = check[2]
                    nw[check[0]][0] = check[2] + 1
                    if check[3] == "A":
                        accepted.append(nw)
                    elif check[3] == "R": # discard range
                        pass
                    else:
                        nw[4] = check[3]
                        new_ranges.append(nw)
                else: # no range gets transferred, continue on
                    pass
            elif check[1] == "<":
                if mx <= check[2]: # means whole range gets transferred
                    if check[3] == "A":
                        accepted.append(rng)
                        return new_ranges
                    elif check[3] == "R": # discard range
                        return new_ranges
                    else:
                        rng[4] = check[3]
                        new_ranges.append(rng)
                        return new_ranges
                elif mn < check[2]: # part of the range gets transfered
                    nw = deepcopy(rng)
                    rng[check[0]][0] = check[2]
                    nw[check[0]][1] = check[2] - 1
                    if check[3] == "A":
                        accepted.append(nw)
                    elif check[3] == "R": # discard range
                        pass
                    else:
                        nw[4] = check[3]
                        new_ranges.append(nw)
                else: # no range gets transferred, continue on
                    pass

ranges = [ [[1,4000], [1,4000], [1,4000], [1,4000], starting_wf_index] ]
accepted = []

while len(ranges) > 0:
    ranges.extend(handle_wf_for_range(ranges.pop(), workflows, accepted))

res = 0
for x in accepted:
    res_range = 1
    for y in x[0:4]:
        res_range *= (y[1] - y[0] + 1)
    res += res_range

print("Part 2:", res)