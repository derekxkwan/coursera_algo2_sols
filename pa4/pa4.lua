gr = {g1={file="g1.txt"},
    g2={file="g2.txt"},
    g3={file="g3.txt"}
    }

local split = "[^%s]+"
local largest = 4e15

loadGraph = function(key)
    --index edges by [tail]head]] = cost so tracks outcoming edges to vert
    print('loading '..key)
    gr[key].edges ={}
    local curline = 0
    for line in io.lines(gr[key].file) do
        local curitem = {}
        for val in string.gmatch(line, split) do
            table.insert(curitem, val)
        end
        if curline == 0 then
            gr[key].numverts = tonumber(curitem[1])
            gr[key].numedges = tonumber(curitem[2])
            curline = curline + 1
        else
            local tail = tonumber(curitem[1])
            local head = tonumber(curitem[2])
            local cost = tonumber(curitem[3])
            --if tail dim doesn't exist, make it
            if gr[key].edges[tail] == nil then
                gr[key].edges[tail] = {}
            end
            --check if edge already exists, if so, choose the min
            local entry
            if gr[key].edges[tail][head] ~= nil then
                entry = math.min(cost,gr[key].edges[tail][head])
            else
                entry = cost
            end
            gr[key].edges[tail][head] = entry
        end
    end
end

bellmanFord = function(key)
    print("running bellman-ford")
    local numedges = gr[key].numedges
    local numverts = gr[key].numverts
    --returns cost array if no neg cycles, returns nil if neg cycles
    local bfedges = {}
    --add new vert 0 with edges to verts in G with cost 0
    bfedges[0] = {}
    for head=1,numverts do
        bfedges[head] = {}
        bfedges[head][0] = 0
    end
    --switch tail and head so tracking incoming edges
    for tail,arr in pairs(gr[key].edges) do
        for head,cost in pairs(arr) do
            if bfedges[head] == nil then
                bfedges[head] = {}
            end
            bfedges[head][tail] = cost
        end
    end

    --run bellman-ford on new vert 0, so A[0,0] = 0, other A[0,_]=inf
    local negcycle = false --if a negative cycle exists
    local A = {} --path cost storage (namely for A[i-1,v] round
    for i=0,numedges do
        local curround = {} --path costs for cur A[i,v] round
        local allequal = true --if curround entries equal to A
        for j=0,numverts do
            if i==0 then
                if j==0 then
                    curround[j] = 0
                else
                    curround[j] = largest
                end
            else
                --first case, prev path goes to curvert
                local pastcost = A[j]
                --second case, prev path goes to one away from curvert
                --loop through all incoming edges
                local mincost = largest
                for tail,cost in pairs(bfedges[j]) do
                    local curcost = A[tail] + cost
                    mincost = math.min(curcost,mincost)
                end
                --take the min of the two cases
                curround[j] = math.min(pastcost,mincost)
                if curround[j] ~= A[j] then
                    allequal = false
                end
            end
        end
        --breaking early
        if i > 0 and allequal == true then
            print('stopping at iteration '..tostring(i))
            break
        elseif i == numedges and allequal == false then
            --negative cycles
            negcycle = true
        end
        --set curround to A (pastround)
        A = curround
    end

    if negcycle == true then
        print(key.." has negative cycles!")
        return nil
    else
        print("finishing bellman-ford")
        return A
    end
end

dijkstra = function(key,source)
    local numedges = gr[key].numedges
    local numverts = gr[key].numverts
    --bounds checking
    if source < 1 or source > numverts then
        return
    end
    --local U = {} --unvisited vert list
    local X = {} --visited verts with true/false
    local A = {} --shortest path costs
    local K = require('heap') --heap of greedy scores A[v] + l_vw
    --init
    for i=1,numverts do
        if i ~= source then
            X[i] = false --mark not visited
            --table.insert(U,i) --add to unvisited
        else
            X[i] = true --mark visited
        end
    end
    --check if source has outgoing edges, if so add to heap, if not return nil
    if gr[key].edges[source] ~= nil then
        for head,cost in pairs(gr[key].edges[source]) do
            --A[src] = 0 so greedy score is l_vw
            K.push({cost, head})
        end
    else
        return nil
    end

    A[source] = 0
    local numvisited = 1 -- number of verts visited
    while numvisited < numverts do
        local curcost
        local curhead
        local edgefound = false
        while edgefound == false do
            --pick min greedy score
            local curedge = K.pop()
            curcost = curedge[1]
            curhead = curedge[2]
            --find idx of curhead in U,
            --if found,  remove it and mark visited. if not, piop a new edge
            if X[curhead] == false then
                X[curhead] = true
                edgefound = true
                numvisited = numvisited + 1
                --[[
                for idx,val in pairs(U) do
                    if curhead == val then
                        table.remove(U,idx)
                        break
                    end
                end
               --]]
            end
        end
        --update shortest path
        A[curhead] = curcost
        --update greedy cost heap
        for head,cost in pairs(gr[key].edges[curhead]) do
            --if head is unvisited, add new edge to heap, else don't bother
            if X[head] == false then
                K.push({curcost+cost,head})
            end
        end
    end

    return A
end

johnsons = function(key)
    local numedges = gr[key].numedges
    local numverts = gr[key].numverts
    local p = bellmanFord(key) --shortest paths
    if p ~= nil then
        print('reweighting edges')
        --reweight vertices if no neg cycles
        for tail,edgearr in pairs(gr[key].edges) do
            for head,cost in pairs(edgearr) do
                local pu = p[tail]
                local pv = p[head]
                gr[key].edges[tail][head] = cost + pu - pv
            end
        end
    else
        return nil
    end
    local shortpaths = {} --shortest paths
    local shortestpath = largest --shortest path of all
    --do dijkstra on each node
    print("running dijkstra")
    for src=1,numverts do
        local curshortest = largest --current shortest path from src
        --find current shortest paths
        local curshorts = dijkstra(key,src)
        --correct shortest path distances from src
        for dest=1,numverts do
            local pu = p[src]
            local pv = p[dest]
            curshorts[dest] = curshorts[dest] - pu + pv
            --find shortest path for this iteration
            curshortest = math.min(curshortest, curshorts[dest])
        end
        --find shortest path overall
        shortestpath = math.min(shortestpath, curshortest)
    end

    --return shortest path of all shortest paths
    return shortestpath
end





--find shortest paths of all shortest paths from all 3 graphs

local ultshort = largest
for key,keyarr in pairs(gr) do
    loadGraph(key)
    local numedges = gr[key].numedges
    local numverts = gr[key].numverts
    print("processing "..key)
    print("numverts: "..tostring(gr[key].numverts)..", numedges: "..tostring(gr[key].numedges))
    local curult = johnsons(key) --find current ultimate shortest path
    if curult ~= nil then
        --min it with ultimate ultimate shortest path
        ultshort = math.min(curult,ultshort)
    end
end

print("shortest path: "..ultshort)

