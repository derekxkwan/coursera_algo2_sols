from UnionFind import UnionFind

def findcandidates(ipt):
    cand = []
    #find all ints 1 and 2 bits away from ipt
    for i in range(bits):  
        i1 = 1<<i #put a one in the ith lsb
        #for 1 bit
        xorval1 = ipt ^ i1
        cand.append(xorval1)
        for j in range(i+1,bits):
            #for 2 bits
            j1 = 1<<j #put a one in the jth lsb
            xorij = i1+j1 #add together to get the val to xor with ipt
            xorval2 = ipt ^ xorij
            cand.append(xorval2)
    return cand


clusters = []
nodes = [] #this will store the nodes as int values, linear time
nodeDict = {}
with open('clustering_big.txt', 'r') as f:
    numNodes, bits = [int(x) for x in f.readline().split(" ")]
    for line in f:
        curval = int('0b'+''.join(line.split(" ")),2)
        nodeDict[str(curval)] = curval
    f.close()

nodes = [int(x) for x in nodeDict.keys()]
for i,node in enumerate(nodes):
    #relabeling nodeDict, i know, not the must efficient... 
    nodeDict[str(node)] = i
numClusters = len(nodes)
print(len(nodes))
nodeUnion = UnionFind(numClusters)


nodeCt = 0
for node in nodes:
    #find neighbors of node where hamdist <= 2
    #then find neighbors of neighbors ,.. recursively

    posscands = findcandidates(node)
    #find the candidates that actually exist
    actualcands = list(set(posscands) & set(nodes))
    #note, nodes are stored in union with their ids
    nodeid = nodeDict[str(node)]
    for cand in actualcands:
        #check roots of node and cand, if not equal, merge them
        rootnode = nodeUnion.find(nodeid)
        candid = nodeDict[str(cand)]
        rootcand = nodeUnion.find(candid)
        if rootnode != rootcand:
            nodeUnion.union(nodeid, candid)
            numClusters -= 1
        
print(numClusters)
'''
#find distances bw each and every node, node^2 time
for i in range(numNodes):
    for j in range(i, numNodes):
        hamdist = bin(nodes[i]^nodes[j]).count("1") #calculating hamming distance bw two nodes
        curedge = (hamdist, i, j)
        hq.heappush(edges,curedge)
'''
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
'''
