w = [.05,.4, .08, .04, .1, .1, .23]
print(w)
n = len(w)
A = [[0 for x in range(n)] for y in range(n)]

for s in range(n):
    for i in range(n-s):
        probterm = sum(w[i:i+s+1])
        curvals = []
        for r in range(i,i+s+1):
           leftidx1 = i
           rightidx1 = r-1
           leftidx2 = r+1
           rightidx2 = i+s
           lefttree = 0
           righttree = 0
           if leftidx1<=  rightidx1:
                lefttree = A[leftidx1][rightidx1]
           if leftidx2 <= rightidx2:
                righttree = A[leftidx2][rightidx2]
           term = probterm + lefttree+righttree
           curvals.append(term)
        A[i][i+s] = min(curvals)
print(A)
print(A[0][n-1])
           
