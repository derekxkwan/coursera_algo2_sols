import math 
numcities = 0
cities = []

with open('tsp.txt', 'r') as f:
    for idx,line in enumerate(f):
        curtext = line.split(' ')
        if idx == 0:
            numcities = int(curtext[0])
        else:
            cities.append({'x': float(curtext[0]), 'y': float(curtext[1])})


def getdist(idx1, idx2):
    return ((cities[idx1]['x']-cities[idx2]['x'])**2 + (cities[idx1]['y']-cities[idx2]['y'])**2)**0.5


def TSP(numcities):
    sidx = 0 #let's make the source index 0
    V = [i for i in range(numcities)] #list of vertices assuming 0 indexing
    numsub = 1 << numcities #number of subsets
    S = [{} for i in range(numcities+1)] #subset array
    for i in range(numsub):
        cursub = [] #current subset
        numitems = 0 #number of items in subset
        for k in range(numcities):
            if i & (1 << k) > 0 and i & 1 > 0:
                #sidx = 0 must be part of this subset
                cursub.append(V[k])
                numitems = numitems + 1
        curstr = " ".join([str(i) for i in cursub]) #string of array for easy indexing
        if numitems > 0:
            S[numitems][curstr] = {'idx': i, 'set': cursub}
    A = {} #soln array
    #init basecases for subset size = 1
    for i in range(numcities):
        A[str(i)] = [float('inf') for j in range(numcities)]
        A[str(i)][i] = 0.
    #now get started with the loops
    for ssize,sstab in enumerate(S): #loop over the first level of S
        for key,entry in sstab.items(): #loop over the entries of the current size
            setstr = " ".join([str(i) for i in entry['set']])
            #if key doesn't exist in A, init
            if setstr not in A:
                A[setstr] = [float("inf") for i in range(numcities)]
            for city in entry["set"]: #loop over city in the subset
                if ssize >= 2 and city != sidx:
                    #temporarily remove city from array
                    curarr = [i for i in entry["set"] if i != city]
                    curstr = " ".join([str(i) for i in curarr])
                    #get entry in soln array
                    curval = float("inf")
                    #loop over possibilities of last hop
                    for hop in curarr:
                        cand = A[curstr][hop] + getdist(hop, city)
                        if cand <= curval:
                            curval = cand
                    A[setstr][city] = curval
    curmin = float('inf') #lets find the minimum path that goes back to the source 0
    finalstr = ' '.join([str(i) for i in range(numcities)])
    for j in range(numcities):
        candval = A[finalstr][j] + getdist(j, sidx)
        if candval <= curmin:
            curmin = candval
    return curmin

print(TSP(numcities))
                    

                
