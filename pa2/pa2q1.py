from UnionFind import UnionFind

edges = []

with open('clustering1.txt', 'r') as f:
    numNodes = int(f.readline())
    for line in f:
        nodescost = [int(x) for x in line.split(" ")]
        #-1 because want to get from 1 index to 0 index
        newedge = {'src': nodescost[0]-1, 'dest': nodescost[1]-1, 'cost':nodescost[2]}
        edges.append(newedge)
    f.close()

edges = sorted(edges, key=lambda k: k['cost'])

numClusters = numNodes
k = 4
verts = UnionFind(numNodes)

while numClusters >= k:
    curedge = edges.pop(0)
    root1 = verts.find(curedge['src'])
    root2 = verts.find(curedge['dest'])
    if root1 != root2:
        verts.union(root1, root2)
        numClusters += -1

print(curedge['cost'])
