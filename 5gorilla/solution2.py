import sys
sys.setrecursionlimit(3500)

alph = input().split()
inv_alph = {ch:i for i,ch in enumerate(alph)}
gain = []
for k in range(len(alph)):
    gain.append([int(x) for x in input().split()])

class Node:
    def __init__(self, cost, type = None, child = None):
        self.cost = cost
        self.child = child
        self.type = type
    def __repr__(self):
        return str(self.type) + ":" + str(self.cost)
    def __lt__(self, other):
        return self.cost < other.cost
    def __add__(self, other):
        return Node(self.cost + other)
    def __sub__(self, other):
        return Node(self.cost - other)

def cost(i,j):
    return gain[inv_alph[s[i]]][inv_alph[t[j]]]

def opt_cost(i,j):
    if i == -1 and j == -1:
        ret = Node(0, type='n')
    elif i == -1:
        ret = Node(-4*(j+1), type='i')
    elif j == -1:
        ret = Node(-4*(i+1), type='j')
    else:
        if mem[i][j]:
            return mem[i][j]
        bres = opt_cost(i-1, j-1)
        lres = opt_cost(i-1, j)
        rres = opt_cost(i, j-1)
        bcost = cost(i,j)
        bret = bres + bcost
        lret = lres - 4
        rret = rres - 4
        maxres = max(bret, lret, rret)
        if maxres == bret:
            ret = bret
            ret.child = bres
            ret.type = 'b'
        elif maxres == lret:
            ret = lret
            ret.child = lres
            ret.type = 'l'
        else:
            ret = rret
            ret.child = rres
            ret.type = 'r'
        mem[i][j] = ret
    return ret

def debug_path(node):
    if not node.child:
        return [node]
    return [node] + debug_path(node.child)

def get_path_string(node, i, j):
    if not node.child:
        if node.type == "n":
            return ("","")
        elif node.type == "i":
            return ((j+1)*"*", t[:j+1])
        else:
            return (s[:i+1], (i+1)*"*")
    if node.type == "b":
        s1, s2 = get_path_string(node.child, i-1, j-1)
        return (s1 + s[i], s2 + t[j])
    elif node.type == "l":
        s1, s2 = get_path_string(node.child, i-1, j)
        return (s1 + s[i], s2 + "*")
    else:
        s1, s2 = get_path_string(node.child, i, j-1)
        return (s1 + "*", s2 + t[j])

def populate_mem():
    for i in range(len(s)):
        for j in range(len(t)):
            opt_cost(i,j)

Q = int(input())
for q in range(Q):
    s,t = input().split()
    mem = [[None for i in range(len(t))] for j in range(len(s))]
    populate_mem()
    res = opt_cost(len(s)-1,len(t)-1)
    print(*get_path_string(res, len(s)-1, len(t)-1))