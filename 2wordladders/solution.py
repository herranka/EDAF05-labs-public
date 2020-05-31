from queue import Queue

class Word:
    def __init__(self, word):
        self.word = word
        self.edges = set()
        self.reset()
    def __repr__(self):
        return self.word
    def reset(self):
        self.visited = False
        self.predecessor = None
    def exists_arc(self, other):
        def occurance(st):
            occ = {}
            for ch in st:
                if ch in occ:
                    occ[ch] += 1
                else:
                    occ[ch] = 1
            return occ
        occ1 = occurance(self.word[1:])
        occ2 = occurance(other.word)
        for ch in occ1.keys():
            if not ch in occ2 or occ2[ch] < occ1[ch]:
                return False
        return True

def path(word):
    if not word.predecessor:
        return []
    return path(word.predecessor) + [word]

def unvisited(edges):
    return (node for node in edges if not node.visited)

def shortest_path(w1, w2, words):
    if w1 == w2:
        return []
    for word in words.values():
        word.reset()
    w1 = words[w1]
    w1.visited = True
    w2 = words[w2]
    q = Queue()
    q.put(w1)
    while not q.qsize() == 0: 
        word = q.get()
        for other in unvisited(word.edges):
            other.visited = True
            other.predecessor = word
            q.put(other)
            if other == w2:
                return path(other)
    return None # no path

def main():
    N, Q = [int(x) for x in input().split()]
    words = {}
    # input
    for n in range(N):
        word = Word(input())
        words[word.word] = word
    # preprocess
    for word in words.values():
        for other in words.values():
            if word == other: continue
            if word.exists_arc(other):
                word.edges.add(other)
    
    for q in range(Q):
        w1, w2 = input().split()
        path = shortest_path(w1, w2, words)
        if path != None:
            print(len(path))
        else:
            print("Impossible")

if __name__ == "__main__":
    main()