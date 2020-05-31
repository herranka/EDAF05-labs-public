import sys
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return str((self.x, self.y))
    def distance_to(self, other):
        return (other.x-self.x)**2 + (other.y-self.y)**2

def half(li):
    mid = math.ceil(len(li)/2)
    return li[:mid], li[mid:]

def split_common(li, lx):
    ly = []
    ry = []
    sx = set(lx)
    for p in li:
        if p in sx:
            ly.append(p)
        else:
            ry.append(p)
    return (ly, ry)

def dist(v1, v2):
    return (v1-v2)**2

def n2_closest(li): # requires two or more items
    m = li[0].distance_to(li[1])
    for i in range(len(li)):
        for j in range(i+1,len(li)):
            d = li[i].distance_to(li[j])
            if d < m:
                m = d
    return m

def filter_pos_y_dist(li, i, d):
    res = []
    for j in range(i+1, len(li)):
        if dist(li[i].y, li[j].y) > d:
            break
        res.append(li[j])
    return res

def closest(px, py, n):
    if n == 2:
        return px[0].distance_to(px[1])
    if n <= 7:
        return n2_closest(px)
    lx, rx = half(px)
    ly, ry = split_common(py, lx)
    cl = closest(lx, ly, len(lx))
    cr = closest(rx, ry, len(rx))
    delta = min(cl, cr)

    # check points between left and right
    linex = (rx[0].x + lx[-1].x)/2
    sy = [p for p in py if dist(p.x, linex) <= delta]
    m = delta
    for i, p1 in enumerate(sy):
        #to_check = [p for p in sy if dist(p1.y, p.y) <= (3/2)*delta and p1.y > p.y] # slow!
        to_check = filter_pos_y_dist(sy, i, (3/2)*delta)
        for p2 in to_check:
            d = p1.distance_to(p2)
            if d < m:
                m = d
    return m

points = []

N = int(input())
for n in range(N):
    x,y = [int(x) for x in input().split()]
    points.append(Point(x,y))

px = sorted(points, key=lambda p: p.x)
py = sorted(points, key=lambda p: p.y)
res = math.sqrt(closest(px, py, len(points)))

print('{:.6f}'.format(round(res, 6)))
