--lua5.3

local split = "[^%s]+"
local curline = 0
local numcity
local cities = {}
for line in io.lines("tsp.txt") do
    local valarr = {}
    for val in string.gmatch(line, split) do
        table.insert(valarr, val)
    end
    if curline == 0 then
        numcity = tonumber(valarr[0])    
    else
        table.insert(cities, {x=valarr[0], y=valarr[1]})
    end
end

local getdist = function(idx1, idx2)
   return math.sqrt((cities[idx1].x-cities[idx2].x)^2 + (cities[idx1].y-cities[idx2]^2)) 
end

function tsp(numverts)
    --sidx = source index, numverts = number of verts (assuming 1-indexing)
    --build a list of vertices not including source index
    local V = {}
    local S = {} --create subsets indexed by size
    for i=1,numverts do
        if i ~= sidx then
            table.insert(V, i)
        end
    end
    local numsub = 1 << (numverts-1) --number of subsets, -1 because adding sidx later
    for m=0,numsub do
        for k=0,(numverts-1) do
        end
    end
end

