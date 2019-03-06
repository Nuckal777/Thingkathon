def vogel(price, production, consumption):
    moves = [[0 for _ in p] for p in price]
    while max(consumption) != 0:
        x,y = select(price, production, consumption)
        print((x,y))
        required = consumption[y]
        existent = production[x]
        delta = min((required, existent))
        consumption[y] -= delta
        production[x] -= delta
        moves[x][y] += delta
        #price[x][y] = -1
        print(delta)
        print("cp")
        print(consumption)
        print(production)
        print("movement")
        print(moves)
        print("price")
        print(price)
        input("")
    return moves

# x-Richtung äußere Liste y-Richtung innere Liste
def select(price, production, consumption):
    diffx = [-7] * len(price)
    diffy = [-7] * len(price[0])
    print("checkprod")
    for x in range(len(price)):
        xRow = price[x].copy()
        if production[x] > 0:
            for y in range(len(price[0])):
                if consumption[y] == 0:
                    xRow.remove(price[x][y])
            min1, min2 = twoMin(xRow)
            diffx[x] = min2 - min1
            print(diffx)
    print("checkcon")
    ylen = len(price[0])
    for y in range(ylen):
        yRow = getRow(price, y).copy()
        if consumption[y] > 0:
            for x in range(len(price)):
                if production[x] == 0:
                    yRow.remove(price[x][y])
            min1, min2 = twoMin(yRow)
            diffy[y] = min2 - min1
            print(diffy)
    maxdiffx = max(diffx, default=-1)
    maxdiffy = max(diffy, default=-1)
    finalx = -1
    finaly = -1
    if maxdiffx > maxdiffy:
        target = price[diffx.index(maxdiffx)].copy()
        smallIndex = 10000
        smallValue = 10000
        for y in range(len(price[0])):
                if consumption[y] != 0:
                    if target[y] < smallValue:
                        smallValue = target[y]
                        smallIndex = y
        miny = y
        finalx = diffx.index(maxdiffx)
        finaly = miny
    else:
        target = getRow(price, diffy.index(maxdiffy)).copy()
        smallIndex = 10000
        smallValue = 10000
        for x in range(len(price)):
                if production[x] != 0:
                    if target[x] < smallValue:
                        smallValue = target[x]
                        smallIndex = x
        minx = smallIndex
        finalx = minx
        finaly = diffy.index(maxdiffy)
    return finalx, finaly

                
def twoMin(l):
    if len(l) == 1:
        return l[0], l[0]
    v1 = min(l)
    lcached = l.copy()
    lcached.remove(v1)
    v2 = min(lcached)
    return v1, v2

def getRow(matrix, index):
    yarray = [0] * len(matrix)
    for x in range(0,len(matrix)):
        yarray[x] = matrix[x][index]
    return yarray

if __name__ == "__main__":
    print(twoMin([2,5,8,9,45,23]))
    price = [[4,1],[2,3],[3,3]]
    prod = [6,15,12]
    con = [13,20]
    x,y = select(price, prod, con)
    print("selected")
    print(price[x][y])
    print(vogel(price, prod, con))