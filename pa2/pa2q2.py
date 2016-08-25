from UnionFind import UnionFind
import heapq as hq

edges = []
nodes = [] #this will store the nodes as int values, linear time
with open('clustering_big.txt', 'r') as f:
    numNodes, bits = [int(x) for x in f.readline().split(" ")]
    nodeCounter = 0
    for line in f:
        curval = int('0b'+''.join(line.split(" ")),2)
        #find distance between curval and vals currently in nodes
        for i in range(len(nodes)):
            hamdist = bin(nodes[i]^curval).count("1") #calculating hamming distance bw two nodes
            curedge = (hamdist, i, nodeCounter)
            hq.heappush(edges,curedge)
        #finally append to nodes and increment nodeCounter
        nodes.append(curval)
        if nodeCounter % 1000 == 0:
            print(nodeCounter)
        nodeCounter += 1
    f.close()

'''
#find distances bw each and every node, node^2 time
for i in range(numNodes):
    for j in range(i, numNodes):
        hamdist = bin(nodes[i]^nodes[j]).count("1") #calculating hamming distance bw two nodes
        curedge = (hamdist, i, j)
        hq.heappush(edges,curedge)
'''

numClusters = numNodes
verts = UnionFind(numNodes)

while True:
    curedge = hq.heappop(edges)
    if curedge[0] >= 3:
        break
    root1 = verts.find(curedge[1])
    root2 = verts.find(curedge[2])
    if root1 != root2:
        verts.union(root1, root2)
        numClusters += -1

print(numClusters)
