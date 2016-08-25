knapitems = []
with open('knapsack1.txt', 'r') as f:
    knapsize, numitems = [int(x) for x in f.readline().split(' ')]
    for line in f:
        curval, curweight = [int(x) for x in line.split(' ')]
        curitem = (curval, curweight)
        knapitems.append(curitem)
    f.close()

A = [[0 for y in range(knapsize + 1)] for x in range(numitems+1)]

#start with i=1 bc A[0,x] = 0 for all x
for i in range(1,numitems+1):
    for x in range(knapsize+1):
        #i-1 because knapitems are 1-indexed
        wi = knapitems[i-1][1] #current weight
        vi = knapitems[i-1][0] #current value
        case1 = A[i-1][x]
        case2 = 0
        if x > wi: #if x - wi >= 0
            case2 = A[i-1][x-wi]+vi
        A[i][x] = max(case1, case2)

print(A[numitems][knapsize])
