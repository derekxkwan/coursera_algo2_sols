import heapq as hq

maxcost = 10000000000000000000000000000000000000.0
with open('edges.txt', 'r') as f:
    nnodes, nedges  = [int(x) for x in f.readline().split(" ")]
    verts = [[] for x in range(nnodes+1)] #1-indexing, verts[0] will be empty
    edges = [{} for x in range(nnodes+1)]
    for line in f:
        node1, node2, cost = [int(x) for x in line.split(" ")]
        #store connected vertices
        verts[node1].append(node2)
        verts[node2].append(node1)
        if node1 > node2:
            temp = node1
            node1 = node2
            node2 = temp
        #store edges by least idx first
        edges[node1][str(node2)] = cost
    f.close()

nonvisited = [int(x) for x in range(1,nnodes)]
visited = [nnodes]
treecost = 0

curheap = [ ]
#init heap

for i, edge in enumerate(edges):
    for node2,cost in edge.items():
        idx1 = i
        idx2 = int(node2)
        if idx1 > idx2:
            temp = idx1
            idx1 = idx2
            idx2 = temp
        tup = (maxcost, idx1, idx2)
        if tup not in curheap:
            hq.heappush(curheap, tup)


def calcheap(node1):
    #print(verts[node1].items())
    for node2 in verts[node1]:
        idx1 = node1
        idx2 = node2
        if idx1 > idx2:
            temp = idx1
            idx1 = idx2
            idx2 = temp
        tup = [y for y in curheap if y[1:] == (idx1, idx2)]
        if node2 in nonvisited:
            cost = edges[idx1][str(idx2)]
            #print(tup)
            if cost < tup[0][0]:
                curheap.remove(tup[0])
                curheap.append((cost, idx1, idx2))
        elif tup:
            curheap.remove(tup[0])
    hq.heapify(curheap)

#print(verts[1])
calcheap(500)
while nonvisited:
    curcost, curnode1, curnode2 = hq.heappop(curheap)
    #print((curcost, curnode1, curnode2))
    if curnode2 not in nonvisited:
        #print("swap")
        curnode2 = curnode1
    nonvisited.remove(curnode2)
    visited.append(curnode2)
    #print(visited)
    treecost += curcost
    calcheap(curnode2)

print(treecost)
