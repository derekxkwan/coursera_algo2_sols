class UnionFind:

    def __init__(self, n):
        self.rank = [0] * n
        self.root = range(n)

    def find(self, i):
        path = []
        curRoot = i
        #finding the root
        while curRoot != self.root[curRoot]:
            path.append(curRoot)
            curRoot = self.root[curRoot]

        #path compression
        for node in path:
            self.root[node] = curRoot

        return curRoot

    def union(self, i, j):
        root1 = self.root[i]
        root2 = self.root[j]
        rank1 = self.rank[root1]
        rank2 = self.rank[root2]
        #if equal, root1 becomes under root2, root2's rank increases by 1
        if rank1 == rank2:
            self.root[root1] = root2
            self.rank[root2] += 1
        #if root1 bigger, root2 becomes under root1
        elif rank1 > rank2:
            self.root[root2] = root1
        else:
            self.root[root1] = root2

    def printRanks(self):
        print(self.rank)

    def printRoots(self):
        print(self.root)

