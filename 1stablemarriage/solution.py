import sys
import re
from queue import Queue

class Person:
    def __init__(self, prefs, i):
        self.prefs = Queue()
        for pref in prefs:
            self.prefs.put(pref)
        self.inverted_prefs = self.inverted_list(prefs)
        self.partner = None
        self.index = i

    def __repr__(self):
        return str(self.index)

    def inverted_list(self, li):
        new = [None] * (N+1)
        for i, el in enumerate(li):
            new[el] = i
        return new

    def prefers(self, other): # prefers other over current partner
        if self.partner == None: 
            return True
        else:
            other_pref = self.inverted_prefs[other.index]
            partner_pref = self.inverted_prefs[self.partner.index]
            return other_pref < partner_pref

def group_n(li, n):
    for i in range(0, len(li), n):
        val = li[i:i+n]
        yield list(val)

def make_person(nums):
    index = nums[0]
    prefs = nums[1:]
    if women[index] == None:
        women[index] = Person(prefs, index)
    elif men[index] == None:
        men[index] = Person(prefs, index)
    # else ignore (eg. 3rd mention)

# för skum indata
read = [int(x) for x in re.split('\s+', sys.stdin.read().strip())]
N = read[0]
men = [None] * (N+1)
women = [None] * (N+1)
lines = group_n(read[1:], N+1)
for nums in lines:
    make_person(nums)

p = Queue()
for m in men:
    if m: p.put(m.index)

while not p.empty():
    m = men[p.get()]
    w = women[m.prefs.get()]
    if w.prefers(m):
        m.partner = w
        if w.partner != None:
            w.partner.partner = None # old partner is now lonely
            p.put(w.partner.index) # put back old partner in queue
        w.partner = m
    else:
        p.put(m.index)

for i, w in enumerate(women[1:]):
    if w == None or w.partner == None:
        print("None")
    else:
        print(w.partner)
