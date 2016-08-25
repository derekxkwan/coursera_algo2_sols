from UnionFind import UnionFind
import heapq as hq

ones = []
edges = []
nodes = [] #this will store the nodes as int values, linear time
with open('clustering_big.txt', 'r') as f:
    numNodes, bits = [int(x) for x in f.readline().split(" ")]
    nodeCounter = 0
    for line in f:
        binstr = '0b'+''.join(line.split(" "))
        curval = int(binstr,2)
        curones = binstr.count("1")

        #find distance between curval and vals currently in nodes
        added = 0 #flag to see if we appended
        for i in range(len(nodes)):
            smallerthan = 1 #flag if cur j node is smaller than each node in nodes[i]
            for j in range(len(nodes[i])):
                curdiff = abs(curones - nodes[i][j][1])
                if curdiff < 3:
                    #calculate hamming distance between two nodes
                    hamdist = bin(curval ^ nodes[i][j][0]).count("1")
                    if hamdist > 2:
                        smallerthan = 0
                        break
                else:
                    smallerthan = 0
                    break
            if smallerthan == 1:
                nodes[i].append((curval, curones))
                added = 1
                break
        if added == 0:
            nodes.append([(curval, curones)])
        #finally append to nodes and increment nodeCounter
        if nodeCounter % 1000 == 0:
            print(nodeCounter)
        nodeCounter += 1
    f.close()

print(len(nodes))
