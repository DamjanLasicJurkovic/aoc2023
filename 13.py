with open("inputs/13.txt") as f:
    inp = f.read()

from copy import deepcopy

def is_mirrored(int_list, pos):
    is_mirrored = True
    sz = len(int_list)
    n = min(pos, sz-pos)
    for i in range(0,n):
        if int_list[pos-1-i] != int_list[pos+i]:
            is_mirrored = False
            break

    return is_mirrored

def compute_score_for_map(rows):
    cols = []
    for i in range(len(rows[0])):
        cols.append("".join([row[i] for row in rows]))
    rows_enumed = [rows.index(x) for x in rows]
    cols_enumed = [cols.index(x) for x in cols]

    # Find mirror positions (n cols/rows before mirror)
    m_pos = [[],[]]
    r_c = [rows_enumed, cols_enumed]
    for r_c_i in range(2):
        for i in range(1,len(r_c[r_c_i])):
            if is_mirrored(r_c[r_c_i], i):
                m_pos[r_c_i].append(i)

    return m_pos

probs = inp.split("\n\n")
    
# Part 1
# Change each input in one int list for rows, one for cols, where same numbers mean identical rows/cols
# list.index returns first occurence so well get the same val for each identical row/col
scores_1 = []
for prob in probs:
    scores_1.append(compute_score_for_map(prob.split("\n")))

print("Part 1:", sum([m_pos[0][0]*100 if len(m_pos[0]) > 0 else m_pos[1][0] for m_pos in scores_1]))

def flip(row, j):
    return row[0:j] + "#."[".#".index(row[j])] + row[j+1::]

def rm_old(sc, sc_old):
    sc1 = deepcopy(sc)
    if len(sc_old[0]) > 0 and sc_old[0][0] in sc1[0]:
        sc1[0].remove(sc_old[0][0])
    if len(sc_old[1]) > 0 and sc_old[1][0] in sc1[1]:
        sc1[1].remove(sc_old[1][0])
    return sc1
    
def is_valid_and_diff_than_old(sc, sc_old):
    sc1 = rm_old(sc, sc_old)
    return (len(sc1[0]) + len(sc1[1])) > 0
    
# Part 2
# Do the same but brute force replace 1 symb per map
scores_2 = []
for i in range(len(probs)):
    rows = probs[i].split("\n")
    for j in range(len(rows)):
        for k in range(len(rows[0])):
            rows[j] = flip(rows[j],k)
            sc = compute_score_for_map(rows)
            rows[j] = flip(rows[j],k)
            if is_valid_and_diff_than_old(sc, scores_1[i]):
                break
        if is_valid_and_diff_than_old(sc, scores_1[i]):
            break
    scores_2.append(sc)

for i in range(len(scores_2)):
    sc1 = scores_1[i]
    scores_2[i] = rm_old(scores_2[i], scores_1[i])
    
print("Part 2:", sum([m_pos[0][0]*100 if len(m_pos[0]) > 0 else m_pos[1][0] for m_pos in scores_2]))