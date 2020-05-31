import sys
sys.setrecursionlimit(4000)

alph = input().split()
inv_alph = {ch:i for i,ch in enumerate(alph)}
cost = []
for k in range(len(alph)):
    cost.append([int(x) for x in input().split()])

class Result:
    def __init__(self, id, cost, strings):
        self.type = id
        self.cost = cost
        self.s = strings[0]
        self.t = strings[1]
    def __lt__(self, other):
        return self.cost < other.cost
    def __add__(self, other):
        return Result(self.type, self.cost + other, [self.s, self.t])
    def __sub__(self, other):
        return Result(self.type, self.cost - other, [self.s, self.t])

def opt(i, j):
    if i == -1 and j == -1:
        return (0, ("", ""))
    elif i == -1:
        return (-4*(j+1), ((j+1)*"*", t[:j+1]))
    elif j == -1:
        return (-4*(i+1), ((s[:i+1]), (i+1)*"*"))
    else:
        if mem[i][j]:
            return mem[i][j]
        bres = Result(0, *opt(i-1, j-1))
        lres = Result(1, *opt(i-1, j))
        rres = Result(2, *opt(i, j-1))
        bcost = cost[inv_alph[s[i]]][inv_alph[t[j]]]
        maxres = max(bres + bcost, lres - 4, rres - 4)
        if maxres.type == 0:
            ret = (maxres.cost, (maxres.s + s[i], maxres.t + t[j]))
        elif maxres.type == 1:
            ret = (maxres.cost, (maxres.s + s[i], maxres.t + "*"))
        else:
            ret = (maxres.cost, (maxres.s + "*", maxres.t + t[j]))
        mem[i][j] = ret
        return ret
    
def populate_mem():
    for i in range(len(s)):
        for j in range(len(t)):
            opt(i,j)

Q = int(input())
for q in range(Q):
    s,t = input().split()
    mem = [[None for i in range(len(t))] for j in range(len(s))]
    populate_mem()
    res = opt(len(s)-1,len(t)-1)
    print(*res[1])