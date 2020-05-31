def binary_search(li, target, cond, i=0, j=None): # assume cond True for low i
    if j == None: j = len(li)-1
    print(i,j)
    if i==j:
        return li[j]
    if i+1 == j:
        if cond(li[j]):
            return li[j]
        else:
            return li[i]
    mid = (i+j)//2
    if cond(li[mid]):
        return binary_search(li, target, cond, mid, j)
    else:
        return binary_search(li, target, cond, i, mid-1)


l = list(range(10))
cond = lambda x: sum(l[:x]) < 24 # example condition
print(binary_search(l, 4, cond))