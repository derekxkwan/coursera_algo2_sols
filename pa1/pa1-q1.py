jobs = []

with open('jobs.txt', 'r') as f:
    numjobs = int(f.readline())
    jobcounter = 1
    for line in f:
        wtln = [int(x) for x in line.split(" ")]
        jobs.append({'jobidx': jobcounter, 'diff':wtln[0]-wtln[1], 'wt':wtln[0], 'ln':wtln[1]})
        jobcounter+=1
    f.close()

jobs.sort(key=lambda x: (x['diff'], x['wt']), reverse=True)

compt = 0 #running completion time
runsum = 0 #running sum
for job in jobs:
    compt += job['ln']
    runsum += compt * job['wt']

print(runsum)
    
        
