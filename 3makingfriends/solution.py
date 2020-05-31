from collections import deque

class Node:
    def __init__(self, id):
        self.id = id
        self.parent = None
        self.size = 0
    def __repr__(self): # debug
        return str(self.id)
    def root(self): # also set all parents to root
        r = self
        s = self
        while r.parent:
            r = r.parent
        while s.parent:
            p = s.parent
            s.parent = r
            s = p
        return r

class Edge:
    def __init__(self, n1, n2, w):
        self.nodes = (n1, n2)
        self.weight = w
    def __lt__(self, other):
        return self.weight < other.weight
    def __repr__(self): # debug
        return str((self.weight, (self.nodes[0], self.nodes[1])))
    def creates_cycle(self):
        return self.nodes[0].root() == self.nodes[1].root()

N, M = [int(x) for x in input().split()]
nodes = [Node(n) for n in range(1, N+1)]
edges = []

for m in range(M):
    u,v,w = [int(x) for x in input().split()]
    edge = Edge(nodes[u-1], nodes[v-1], w)
    edges.append(edge)

edges = sorted(edges, key=lambda x: x.weight)
edges = deque(edges)

def union(u, v):
    ur = u.root()
    vr = v.root()
    if ur.size < vr.size:
        ur.parent = vr
        vr.size = ur.size + vr.size
    else:
        vr.parent = ur
        ur.size = ur.size + vr.size

#def union(u, v):
#    u.root().parent = v

#def union(u,v):
#    u.parent = v

def kruskal(nodes, edges):
    sum = 0
    count = 0
    while edges and count < len(nodes)-1: # max n-1 edges
        edge = edges.popleft()
        if not edge.creates_cycle():
            sum += edge.weight
            union(*edge.nodes)
            count += 1
    return sum

total_weight = kruskal(nodes, edges)

print(total_weight)