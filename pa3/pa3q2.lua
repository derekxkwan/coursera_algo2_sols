--lua5.2
local res = {}
local optimal
local knapitems = {}
local calcknap
local knapsize
local knapwt
calcknap = function (itemno, curwt)
    if itemno < 1 then
        return 0
    end
    local curstr = tostring(itemno)..","..tostring(curwt)
    if res[curstr] ~= nil then
        return res[curstr]
    else
        local itemval = knapitems[itemno]["val"]
        local itemwt = knapitems[itemno]["wt"]
        local newitemno = itemno - 1
        local str1 = tostring(newitemno)..","..tostring(curwt)
        local term1
        if res[str1] ~= nil then
            term1 = res[str1]
        else
            term1 = calcknap(newitemno, curwt)
            res[str1] = term1
        end
        if curwt < itemwt then
            return term1
        else
            local term2
            local newwt = curwt - itemwt
            local str2 = tostring(newitemno)..","..tostring(newwt)
            if res[str2] ~= nil then
                term2 = res[str2]
            else
                term2 = calcknap(newitemno, newwt)
                res[str2] = term2
            end
            local retval = math.max(term1,term2+itemval)
            res[curstr] = retval
            return retval
        end
    end
end

local split = "[^%s]+"
local file = "knapsack_big.txt"
local lineno = 0
for line in io.lines(file) do
    local curnum = 1
    local curitem = {}
    for val in string.gmatch(line, split) do
        curitem[curnum] = val
        curnum = curnum + 1
    end
    if lineno == 0 then
        knapwt = tonumber(curitem[1])
        knapsize = tonumber(curitem[2])
    else
        local itemval = tonumber(curitem[1])
        local itemwt = tonumber(curitem[2])
        local toadd = {val=itemval,wt=itemwt}
        knapitems[lineno] = toadd
    end
    --print(lineno)
    lineno = lineno + 1
end

optimal = calcknap(knapsize, knapwt)
print(optimal)
