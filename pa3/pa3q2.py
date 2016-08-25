import sys

knapitems = []
with open('knapsack_big.txt', 'r') as f:
    knapsize, numitems = [int(x) for x in f.readline().split(' ')]
    minweight = 100000000000
    for line in f:
        curval, curweight = [int(x) for x in line.split(' ')]
        minweight = min(minweight, curweight)
        curitem = (curval, curweight)
        knapitems.append(curitem)
    f.close()

sys.setrecursionlimit(max(knapsize, numitems)*10)
A = {}


def calcKnapsack(itemno, weight):
    if itemno <= -1 or weight < minweight:
        return 0
    curstr = str(itemno) + "," + str(weight)
    if curstr in A.keys():
        return A[curstr]
    else:
        curval = knapitems[itemno][0]
        curweight = knapitems[itemno][1]
        newitemno = itemno-1
        term1str = str(newitemno) + "," + str(weight)
        if term1str in A.keys():
            term1 = A[term1str]
        else:
            term1 = calcKnapsack(newitemno, weight)
            A[term1str] = term1
        if curweight > weight:
            A[curstr] = term1
            return term1
        else:
            newweight = weight-curweight
            term2str = str(newitemno) + "," + str(newweight)
            if term2str in A.keys():
                term2 = A[term2str]
            else:
                term2 = calcKnapsack(newitemno, newweight) + curval
                A[term2str] = term2
            retval = max(term1, term2)
            A[curstr] = retval
            return retval

returnval = calcKnapsack(numitems-1, knapsize)
print(returnval)
        
        
