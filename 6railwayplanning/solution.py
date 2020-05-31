import sys
from math import log2, ceil

class Node:
    def __init__(self, id):
        self.id = id
        self.edges = set()
        self.visited = False
        self.origin_edge = None
    def __repr__(self):
        return str(self.id)
    def reset(self):
        # don't reset flows, only path
        self.visited = False
        self.origin_edge = None
    def pred(self):
        if self.origin_edge:
            return self.origin_edge.other(self)
        return None

class Edge:
    def __init__(self, n1, n2, capacity):
        self.source = n1
        self.target = n2
        self.capacity = capacity
        self.flow = 0
    def __repr__(self):
        return "(%s->%s:%d/%d)" % (self.source, self.target, self.flow, self.capacity)
    def reset(self):
        self.flow = 0
    def remaining_from(self, node):
        if node == self.source:
            return self.remaining_forward()
        else:
            return self.remaining_backward()
    def remaining_forward(self):
        return self.capacity - self.flow
    def remaining_backward(self):
        return self.capacity + self.flow
    def other(self, node):
        if node == self.source:
            return self.target
        else:
            return self.source
    def origin_node(self):
        if self.source.origin_edge == self:
            return self.target
        else:
            return self.source
    def add_flow_from(self, node, d):
        if node == self.source:
            self.flow += d
        else:
            self.flow -= d

N,M,C,P = [int(x) for x in input().split()]
nodes = [Node(n) for n in range(N)]
edges = []
for m in range(M):
    u,v,c = [int(x) for x in input().split()]
    edge = Edge(nodes[u], nodes[v], c)
    nodes[u].edges.add(edge)
    nodes[v].edges.add(edge)
    edges.append(edge)

def remove_edge(edge):
    s = edge.source.edges
    t = edge.target.edges
    if edge in s:
        s.remove(edge)
    if edge in t:
        t.remove(edge)

def redraw_edge(edge):
    edge.source.edges.add(edge)
    edge.target.edges.add(edge)

def get_path(node):
    ret = []
    cur = node
    while cur.origin_edge:
        e = cur.origin_edge
        ret.append(e)
        cur = cur.pred()
    return ret[::-1]

def delta(path):
    if not path:
        return 0
    d = path[0].remaining_from(path[0].origin_node())
    for e in path:
        origin = e.origin_node()
        remaining = e.remaining_from(origin)
        if remaining < d:
            d = remaining
    return d

def add_flow(path, d):
    for e in path:
        origin = e.origin_node()
        e.add_flow_from(origin, d)

def max_flow(nodes):
    return sum([e.flow for e in nodes[0].edges])

def shortest_path(nodes, min_remaining):
    for node in nodes:
        node.reset()
    q = [nodes[0]]
    nodes[0].visited = True
    for cur in q:
        for edge in cur.edges:
            target = edge.other(cur)
            remaining = edge.remaining_from(cur)
            if target.visited or remaining < min_remaining or remaining == 0: # remove last cond?
                continue
            target.visited = True
            target.origin_edge = edge
            q.append(target)
            if target == nodes[-1]: # is target
                return get_path(target)
    return [] # no path found

def find_max_flow(nodes, edges):
    for edge in edges:
        edge.reset()
    path = ["höhö"]
    x = 2**int(ceil(log2(C)))
    while x >= 1:
        path = shortest_path(nodes, x)
        if not path:
            x /= 2
            continue
        d = delta(path)
        add_flow(path, d)
    return max_flow(nodes)


def find_max_flow_with_index(nodes, edges, to_remove, index): # remove everything up to i in to_remove
    for i in range(index+1):
        yeet = edges[to_remove[i]]
        remove_edge(yeet)
    for i in range(index+1,len(to_remove)):
        stonks = edges[to_remove[i]]
        redraw_edge(stonks)
    mf = find_max_flow(nodes, edges)
    return mf

def binary_search(li, results = None, i=0, j=None): # assume cond True for low i
    if results == None:
        results = [None for x in range(len(li))]
    if j == None: j = len(li)-1
    def calc(index):
        if results[index] != None:
            return results[index]
        else:
            res = find_max_flow_with_index(nodes, edges, li, index)
            results[index] = res
            return res
    def cond(index):
        res = calc(index)
        return res >= C
    if i==j:
        return j+1, calc(j)
    if i+1 == j:
        if cond(j):
            return j+1, calc(j)
        else:
            return i+1, calc(i)
    mid = (i+j)//2
    if cond(mid):
        return binary_search(li, results, mid, j)
    else:
        return binary_search(li, results, i, mid-1)


to_remove = [int(input()) for p in range(P)]
p, prev_flow = binary_search(to_remove)


"""
prev_flow = -1
for p in range(P):
    to_remove = int(input())
    remove_edge(edges[to_remove])
    flow = find_max_flow(nodes, edges)
    #print("%d: max flow found" % p)
    if flow < C:
        break
    prev_flow = flow
"""

print(p, prev_flow)