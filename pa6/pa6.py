import sys

#files = ["test1.txt", "test2.txt"]
files = ["2sat1.txt", "2sat2.txt", "2sat3.txt", "2sat4.txt", "2sat5.txt", "2sat6.txt"]
tsat = {}

'''
convert clauses to graphs
each var and its negation has its own vertex
let 2*x be the var number and 2*x+1 be its negation
for uVv: add ~u->v and ~v -> u

a 2-CNF is unsatisfiable iff there exists a var x st
there is a path from x to ~x (and likewise ~x to x)

thus find paths between x and ~x (and vice versa), reject if found for any var x

'''

def varToVert(varnum):
    #convert from variable number to vert number
    #first reindex from 1-idx to 0-idx
    if varnum >= 0:
        return (varnum - 1) * 2
    if varnum < 0:
        return 1 + (-1 * (varnum+ 1))*2

def loadFiles():
    for fname in files:
        gname = fname.split(".")[0] #use filename -txt as the graphname
        tsat[gname] = {}
        with open(fname, "r") as f:
            for idx,line in enumerate(f):
                curstr = [int(i) for i in line.split(" ")]
                if idx == 0:
                    n = 2*curstr[0]
                    tsat[gname]['n'] = n #number of vertices = (number of vars * 2)
                    #init graph arrays, grev = graph reversed, g = regular graph
                    tsat[gname]['grev'] = [[] for i in range(n)]
                    tsat[gname]['g'] = [[] for i in range(n)]
                else:
                    #graphs will be in g[tail][head] format
                    u = varToVert(curstr[0])
                    notu = varToVert(-1*curstr[0])
                    v = varToVert(curstr[1])
                    notv = varToVert(-1*curstr[1])
                    tsat[gname]['g'][notu].append(v)
                    tsat[gname]['grev'][v].append(notu)
                    tsat[gname]['g'][notv].append(u)
                    tsat[gname]['grev'][u].append(notv)

def revDFS(gname, sidx):
    n = tsat[gname]['n']
    tsat[gname]['visited'][sidx] = True
    tsat[gname]['nvis'] = tsat[gname]['nvis'] + 1 #increment number visited
    for head in tsat[gname]['grev'][sidx]:
        if tsat[gname]['visited'][head] == False and tsat[gname]['nvis'] < n:
            #add condition to break early
            revDFS(gname, head)
    tsat[gname]['stack'][:0] = [sidx]


def revDFSLoop(gname): 
    n = tsat[gname]['n']
    tsat[gname]['stack'] = [] #vertex stack
    tsat[gname]['visited'] = [False for i in range(n)] #visited verts
    tsat[gname]['nvis'] = 0 #number of verts visited
    for node in range(n):
        if tsat[gname]['nvis'] >= n: #break early
            break
        if tsat[gname]['visited'][node] == False:
            revDFS(gname, node)

def fwdDFS(gname, sidx, top):
    n = tsat[gname]['n']
    tsat[gname]['visited'][sidx] = True
    tsat[gname]['nvis'] = tsat[gname]['nvis'] + 1 #increment number visited
    #record top idx of scc
    tsat[gname]['scc'][sidx] = top
    for head in tsat[gname]['g'][sidx]:
        if tsat[gname]['visited'][head] == False and tsat[gname]['nvis'] < n:
            #add condition to break early
            fwdDFS(gname,head,top)

                                
def fwdDFSLoop(gname):
    n = tsat[gname]['n']
    tsat[gname]['visited'] = [False for i in range(n)] #visited verts
    tsat[gname]['scc'] = [-1 for i in range(n)] #scc leaders
    tsat[gname]['nvis'] = 0 #number of verts visited
    for node in tsat[gname]['stack']:
        if tsat[gname]['nvis'] >= n: #break early
            break
        if tsat[gname]['visited'][node] == False:
            fwdDFS(gname, node, node)

def twosat(gname):
    n = tsat[gname]['n']
    revDFSLoop(gname)
    fwdDFSLoop(gname)
    #check if x and ~x are in the same scc
    satis = True
    for i in xrange(0,n,2):
        if tsat[gname]['scc'][i] == tsat[gname]['scc'][i+1]:
            #if x and ~x in the same scc, break
            satis = False
            break
    return satis

loadFiles()
for gname in tsat.keys():
    cursat = twosat(gname)
    print(gname + ': ' + str(cursat))
