with open("inputs/12.txt") as f:
    inp = f.read()

from copy import deepcopy

recs = [[y for y in x.split(" ")] for x in inp.split("\n")]
for x in recs:
    x[0] = eval("[" + x[0].replace(".", "0, ").replace("#", "1, ").replace("?", "2, ") + "]")
    x[1] = eval("[" + x[1] + "]")

# Shamelessly using code from https://replit.com/@smichr/msp for computing multiset permutations
def msp(items):
  '''Yield the permutations of `items` where items is either a list
  of integers representing the actual items or a list of hashable items.
  The output are the unique permutations of the items given as a list
  of integers 0, ..., n-1 that represent the n unique elements in
  `items`.

  Examples
  ========

  >>> for i in msp('xoxox'):
  ...   print(i)

  [1, 1, 1, 0, 0]
  [0, 1, 1, 1, 0]
  [1, 0, 1, 1, 0]
  [1, 1, 0, 1, 0]
  [0, 1, 1, 0, 1]
  [1, 0, 1, 0, 1]
  [0, 1, 0, 1, 1]
  [0, 0, 1, 1, 1]
  [1, 0, 0, 1, 1]
  [1, 1, 0, 0, 1]

  Reference: "An O(1) Time Algorithm for Generating Multiset Permutations", Tadao Takaoka
  https://pdfs.semanticscholar.org/83b2/6f222e8648a7a0599309a40af21837a0264b.pdf
  '''

  def visit(head):
      (rv, j) = ([], head)
      for i in range(N):
          (dat, j) = E[j]
          rv.append(dat)
      return rv

  u = list(set(items))
  E = list(reversed(sorted([u.index(i) for i in items])))
  N = len(E)
  # put E into linked-list format
  (val, nxt) = (0, 1)
  for i in range(N):
      E[i] = [E[i], i + 1]
  E[-1][nxt] = None
  head = 0
  afteri = N - 1
  i = afteri - 1
  yield visit(head)
  while E[afteri][nxt] is not None or E[afteri][val] < E[head][val]:
      j = E[afteri][nxt]  # added to algorithm for clarity
      if j is not None and E[i][val] >= E[j][val]:
          beforek = afteri
      else:
          beforek = i
      k = E[beforek][nxt]
      E[beforek][nxt] = E[k][nxt]
      E[k][nxt] = head
      if E[k][val] < E[head][val]:
          i = k
      afteri = E[i][nxt]
      head = k
      yield visit(head)

# Part 1
# Combine all possible multiset computations for "?"s based on number of total "#"s
# Try them all and count the working ones
def is_legit(vals, seq):
    exp_seq = []
    exp_1 = 0
    for i in range(len(vals)):
        if vals[i] == 0 and exp_1 != 0:
            exp_seq.append(exp_1)
            exp_1 = 0
        if vals[i] == 1:
            exp_1 += 1
    if exp_1 != 0:
        exp_seq.append(exp_1)
    return exp_seq == seq

def get_permutations(rec, seq):
    n_ones = sum(seq) - rec.count(1)
    len_perm = rec.count(2)
    if n_ones == len_perm:
        return [[1]*n_ones]
    else:
        multiset = [1]*n_ones + [0]*(len_perm-n_ones)
        return msp(multiset)

def generate_new_with_perm(rec, repl):
    ret = deepcopy(rec)
    count = 0
    for i in range(len(ret)):
        if ret[i] == 2:
            ret[i] = repl[count]
            count += 1
    return ret

nr_possible = []
for rec in recs:
    n = 0
    for perm in get_permutations(rec[0], rec[1]):
        if (is_legit(generate_new_with_perm(rec[0], perm), rec[1])):
            n += 1
    nr_possible.append(n)

print("Part 1:", sum(nr_possible))
