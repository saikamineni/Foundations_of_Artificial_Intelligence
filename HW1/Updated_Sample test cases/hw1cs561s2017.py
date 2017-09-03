import copy
from collections import OrderedDict

# Creating empty matrix for weights
wt = [[0 for i in range(8)]for j in range(8)] 

# Assigning weights
wt[0] = wt[7] = [99, -8, 8, 6, 6, 8, -8, 99]
wt[1] = wt[6] = [-8, -24, -4, -3, -3, -4, -24, -8]
wt[2] = wt[5] = [8, -4, 7, 4, 4, 7, -4, 8]
wt[3] = wt[4] = [6, -3, 4, 0, 0, 4, -3, 6]


# Creating empty matrix for input
root = [[0 for i in range(8)]for j in range(8)]

# counter to check first two rows in file
count = 0

# store player, depth and initial state
with open("input.txt") as f:
    for line in f:
        if count==0:
            who = line[:-1]
        elif count==1:
            d = int(line[:-1])
        else:
            root[count-2] = list(line)[0:8]
        count += 1
f.close() 
depth = [None] * (d+1)
depth[0] = OrderedDict.fromkeys(['root'])
depth[0]['root'] = root

depth_values = [None] * (d+1)
total_count = []
op = open("output.txt", 'w')
# calculate total weight
def calcEval(p, ip):
    val = 0
    for i in range(8):
        for j in range(8):
            if ip[i][j]==p:
                val+=wt[i][j]
    return val

# prints grid

def printGrid(ip):
    for row in ip:
        #print "".join(row)
        op.write("".join(row))
        op.write("\n")
    #print "\n"
    op.write("Node,Depth,Value,Alpha,Beta\n")

def printStatements(key, i, v, alpha, beta):
    actual_key = key.rsplit('-',1)[-1]
    
    if v == float('-inf'):
        v1 = "-Infinity"
    elif v == float('inf'):
        v1 = "Infinity"
    else:
        v1 = v
    
    if alpha == float('-inf'):
        alpha1 = "-Infinity"
    elif alpha == float('inf'):
        alpha1 = "Infinity"
    else:
        alpha1 = alpha
    
    if beta == float('-inf'):
        beta1 = "-Infinity"
    elif beta == float('inf'):
        beta1 = "Infinity"
    else:
        beta1 = beta
    
    #print actual_key+"," + str(i) + "," + str(v1) + "," + str(alpha1) + "," + str(beta1)
    op.write(actual_key+"," + str(i) + "," + str(v1) + "," + str(alpha1) + "," + str(beta1)+"\n")
    


def renamePos(row, col):
    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    return alpha[col] + str(row+1)



def getPos(pos):
    alpha = [('a',0), ('b',1), ('c',2), ('d',3), ('e',4), ('f',5), ('g',6), ('h',7)]
    for ele in alpha:
        if pos[0] == ele[0]:
            return ((int(pos[1])-1, ele[1]))


nextNodes = []
nextNums = []
elem = []

# search opponent position vertically
def searchXVer(row, col, ip):
    global nextNums
    val1 = 'X'
    val2 = 'O'
    i=row
    j=col
    while (i>=1):
        i = i - 1
        if ip[i][j]==val1:
            continue
        elif (i<row-1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break      
                
    i=row
    while (i<7):
        i = i + 1
        if ip[i][j]==val1:
            continue
        elif (i>row+1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break
    return
        
# search opponent position horizontally
def searchXHor(row, col, ip):
    global nextNums
    val1 = 'X'
    val2 = 'O'
    i=row
    j=col
    while (j>=1):
        j = j - 1
        if ip[i][j]==val1:
            continue
        elif (j<col-1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break 
                
    j=col
    while (j<7):
        j = j + 1
        if ip[i][j]==val1:
            continue
        elif (j>col+1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break
    return
                
# search opponent position diagonally
def searchXDia(row, col, ip):
    global nextNums
    val1 = 'X'
    val2 = 'O'
    i=row-1
    j=col-1
    while((i>=0) and (j>=0)) and ((i<8) and (j<8)):
        if ip[i][j]==val1:
            i = i - 1
            j = j - 1
            continue
        elif (j<col-1) or (i<row-1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break
        i = i - 1
        j = j - 1
        
    i=row+1
    j=col+1
    while((i>=0) and (j>=0)) and ((i<8) and (j<8)):
        if ip[i][j]==val1:
            i = i + 1
            j = j + 1
            continue
        elif (j>col+1) or (i>row+1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break
        i = i + 1
        j = j + 1
        
    i=row-1
    j=col+1
    while((i>=0) and (j>=0)) and ((i<8) and (j<8)):
        #print "DiaSU"
        #print i,j
        if ip[i][j]==val1:
            i = i - 1
            j = j + 1
            continue
        elif (j>col+1) or (i>row+1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break
        i = i - 1
        j = j + 1

    i=row+1
    j=col-1
    while((i>=0) and (j>=0)) and ((i<8) and (j<8)):
        if ip[i][j]==val1:
            i = i + 1
            j = j - 1
            continue
        elif (j>col+1) or (i>row+1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break
        i = i + 1
        j = j - 1
    return


# search opponent position vertically
def searchOVer(row, col, ip):
    global nextNums
    val1 = 'X'
    val2 = 'O'
    i=row
    j=col
    while (i>=1):
        i = i - 1
        if ip[i][j]==val2:
            continue
        elif (i<row-1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break      
                
    i=row
    while (i<7):
        i = i + 1
        if ip[i][j]==val2:
            continue
        elif (i>row+1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break 
    return
        
# search opponent position horizontally
def searchOHor(row, col, ip):
    global nextNums
    val1 = 'X'
    val2 = 'O'
    i=row
    j=col
    while (j>=1):
        j = j - 1
        if ip[i][j]==val2:
            continue
        elif (j<col-1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break 
                
    j=col
    while (j<7):
        j = j + 1
        if ip[i][j]==val2:
            continue
        elif (j>col+1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break
    return
                
# search opponent position diagonally
def searchODia(row, col, ip):
    global nextNums
    val1 = 'X'
    val2 = 'O'
    i=row-1
    j=col-1
    while((i>=0) and (j>=0)) and ((i<8) and (j<8)):
        if ip[i][j]==val2:
            i = i - 1
            j = j - 1
            continue
        elif (j<col-1) or (i<row-1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break
        i = i - 1
        j = j - 1
        
    i=row+1
    j=col+1
    while((i>=0) and (j>=0)) and ((i<8) and (j<8)):
        if ip[i][j]==val2:
            i = i + 1
            j = j + 1
            continue
        elif (j>col+1) or (i>row+1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break
        i = i + 1
        j = j + 1
        
    i=row-1
    j=col+1
    while((i>=0) and (j>=0)) and ((i<8) and (j<8)):
        if ip[i][j]==val2:
            i = i - 1
            j = j + 1
            continue
        elif (j>col+1) or (i>row+1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break
        i = i - 1
        j = j + 1

    i=row+1
    j=col-1
    while((i>=0) and (j>=0)) and ((i<8) and (j<8)):
        if ip[i][j]==val2:
            i = i + 1
            j = j - 1
            continue
        elif (j>col+1) or (i>row+1):
            if ip[i][j]=='*':
                nextNums.append((i,j))
            break
        else:
            break
        i = i + 1
        j = j - 1
    return
        


def sortOrder():
    global nextNodes
    global elem
    global nextNums
    if len(nextNums)>1:
        rows = []
        for ele in nextNums:
            rows.append(ele[0])
        count = 0
        for i in range(min(rows), max(rows)+1):
            elem_temp = []
            for tup in nextNums:
                if tup[0] == i:
                    elem_temp.append(tup)
            if count%2 == 0:
                elem=elem + sorted(elem_temp, key=lambda x: x[1])
            else:
                elem=elem + sorted(elem_temp, key=lambda x: x[1], reverse=True)
            count+=1
        for ele in elem:
            nextNodes.append(renamePos(ele[0], ele[1]))
    elif len(nextNums)==1:
        nextNodes.append(renamePos(nextNums[0][0], nextNums[0][1]))
    return

# logic

# search for player position
def searchXPos(ip):
    global nextNodes
    global nextNums
    for i in range(8):
        for j in range(8):
            if ip[i][j]=='X':
                r = i
                c = j
                #print "first"
                #print i,j
                searchOVer(r, c, ip)
                searchOHor(r, c, ip)
                searchODia(r, c, ip)
    sortOrder()
    return


def searchOPos(ip):
    global nextNodes
    global nextNums
    for i in range(8):
        for j in range(8):
            if ip[i][j]=='O':
                r = i
                c = j
                #print "first"
                #print i,j
                searchXVer(r, c, ip)
                searchXHor(r, c, ip)
                searchXDia(r, c, ip)
    sortOrder()
    return


# change the values of O's and place X's
def findOHor(row, col, ip, inter):
    val1 = 'X'
    val2 = 'O'
    for i in range(8):
        for j in range(8):
            if ip[i][j]==val1:
                if row == i:
                    inter[row][col]=val1
                    c1 = j
                    j1 = j
                    if (c1 < col):
                        while (j1<=col):
                            if ip[i][j1]==val2:
                                inter[i][j1]=val1
                            j1 = j1 + 1
                    else:
                        while (j1>=col):
                            if ip[i][j1]==val2:
                                inter[i][j1]=val1
                            j1 = j1 - 1
    return inter


def findOVer(row, col, ip, inter):
    val1 = 'X'
    val2 = 'O'
    for i in range(8):
        for j in range(8):
            if ip[i][j]==val1:
                if col == j:
                    inter[row][col]=val1
                    r1 = i
                    i1=i
                    if (r1 < row):
                        while (i1<=row) and (i1>=0):
                            if ip[i1][j]==val2:
                                inter[i1][j]=val1
                            i1 = i1 + 1
                    else:
                        while (i1>=row) and (i1<=7):
                            if ip[i1][j]==val2:
                                inter[i1][j]=val1
                            i1 = i1 - 1
    return inter


def findODia(row, col, ip, inter):
    val1 = 'X'
    val2 = 'O'
    for i in range(8):
        for j in range(8):
            if ip[i][j]==val1:
                if abs(row-i) == abs(col-j):
                    r1=i
                    c1=j
                    if (row-i)>0 and (col-j)>0:
                        inter[row][col]=val1
                        while(r1<row) and (c1<col):
                            if ip[r1][c1]==val2:
                                inter[r1][c1]=val1
                            r1 = r1 + 1
                            c1 = c1 + 1
                    elif (row-i)>0 and (col-j)<0:
                        inter[row][col]=val1
                        while(r1<row) and (c1>col):
                            if ip[r1][c1]==val2:
                                inter[r1][c1]=val1
                            r1 = r1 + 1
                            c1 = c1 - 1
                    elif (row-i)<0 and (col-j)<0:
                        inter[row][col]=val1
                        while(r1>row) and (c1>col):
                            if ip[r1][c1]==val2:
                                inter[r1][c1]=val1
                            r1 = r1 - 1
                            c1 = c1 - 1
                    elif (row-i)<0 and (col-j)>0:
                        inter[row][col]=val1
                        while(r1>row) and (c1<col):
                            if ip[r1][c1]==val2:
                                inter[r1][c1]=val1
                            r1 = r1 - 1
                            c1 = c1 + 1
    return inter


# change the values of X's and place S's
def findXHor(row, col, ip, inter):
    val1 = 'O'
    val2 = 'X'
    for i in range(8):
        for j in range(8):
            if ip[i][j]==val1:
                if row == i:
                    inter[row][col]=val1
                    c1 = j
                    j1 = j
                    if (c1 < col):
                        while (j1<=col):
                            if ip[i][j1]==val2:
                                inter[i][j1]=val1
                            j1 = j1 + 1
                    else:
                        while (j1>=col):
                            if ip[i][j1]==val2:
                                inter[i][j1]=val1
                            j1 = j1 - 1
    return inter


def findXVer(row, col, ip, inter):
    val1 = 'O'
    val2 = 'X'
    for i in range(8):
        for j in range(8):
            if ip[i][j]==val1:
                if col == j:
                    inter[row][col]=val1
                    r1 = i
                    i1=i
                    if (r1 < row):
                        while (i1<=row):
                            if ip[i1][j]==val2:
                                inter[i1][j]=val1
                            i1 = i1 + 1
                    else:
                        while (i1>=row):
                            if ip[i1][j]==val2:
                                inter[i1][j]=val1
                            i1 = i1 - 1
    return inter


def findXDia(row, col, ip, inter):
    val1 = 'O'
    val2 = 'X'
    for i in range(8):
        for j in range(8):
            if ip[i][j]==val1:
                if abs(row-i) == abs(col-j):
                    r1=i
                    c1=j
                    if (row-i)>0 and (col-j)>0:
                        inter[row][col]=val1
                        while(r1<row) and (c1<col):
                            if ip[r1][c1]==val2:
                                inter[r1][c1]=val1
                            r1 = r1 + 1
                            c1 = c1 + 1
                    elif (row-i)>0 and (col-j)<0:
                        inter[row][col]=val1
                        while(r1<row) and (c1>col):
                            if ip[r1][c1]==val2:
                                inter[r1][c1]=val1
                            r1 = r1 + 1
                            c1 = c1 - 1
                    elif (row-i)<0 and (col-j)<0:
                        inter[row][col]=val1
                        while(r1>row) and (c1>col):
                            if ip[r1][c1]==val2:
                                inter[r1][c1]=val1
                            r1 = r1 - 1
                            c1 = c1 - 1
                    elif (row-i)<0 and (col-j)>0:
                        inter[row][col]=val1
                        while(r1>row) and (c1<col):
                            if ip[r1][c1]==val2:
                                inter[r1][c1]=val1
                            r1 = r1 - 1
                            c1 = c1 + 1
    return inter


def changeO(val, i, ip):
    global depth
    for ele in nextNodes:
        (row,col) = getPos(ele)
        depth[i][val+ele]=copy.deepcopy(ip)
        depth[i][val+ele] = findOHor(row, col, ip, depth[i][val+ele])
        depth[i][val+ele] = findOVer(row, col, ip, depth[i][val+ele])
        depth[i][val+ele] = findODia(row, col, ip, depth[i][val+ele])
        

def changeX(val, i, ip):
    global depth
    for ele in nextNodes:
        (row,col) = getPos(ele)
        depth[i][val+ele]=copy.deepcopy(ip)
        depth[i][val+ele] = findXHor(row, col, ip, depth[i][val+ele])
        depth[i][val+ele] = findXVer(row, col, ip, depth[i][val+ele])
        depth[i][val+ele] = findXDia(row, col, ip, depth[i][val+ele])
        
 
def getTotalValues():
    global total_count
    i=0
    for i in range(d+1):
        for key in depth[i].keys():
            if i==d:
                total_count.append((key,0))
            else:
                count=0
                for key1 in depth[i+1].keys():
                    if key1.startswith(key):
                        count+=1
                total_count.append((key,count))

    total_count = OrderedDict(total_count)
    return

def updateDepthValues():
    global depth_values
    depth_values = copy.deepcopy(depth)    
    for i in range(d+1):
        if i==d:
            if who == 'X':
                for key in depth_values[i].keys():
                    depth_values[i][key] = [calcEval('X', depth[i][key]) - calcEval('O', depth[i][key]), float('-inf'), float('inf'), total_count[key]]
            else:
                for key in depth_values[i].keys():
                    depth_values[i][key] = [calcEval('O', depth[i][key]) - calcEval('X', depth[i][key]), float('-inf'), float('inf'), total_count[key]]
        else:
            if i%2==0:
                for key in depth_values[i].keys():
                    depth_values[i][key] = [float('-inf'), float('-inf'), float('inf'), total_count[key]]
            else:
                for key in depth_values[i].keys():
                    depth_values[i][key] = [float('inf'), float('-inf'), float('inf'), total_count[key]]
    return

def alphabeta():
    #for who = X
    # initial parsing till terminal node
    i=0
    p=1
    for i in range(d):
        p=1
        for key in depth_values[i].keys():
            if p==1:
                p=0
                depth_values[i][key][3]-=1
                #printStatements(key, i, depth_values[i][key][0], depth_values[i][key][1], depth_values[i][key][2])
    i+=1        
    while depth_values[0]['root'][3]>=-1 and i>=0:
        #count-=1
        for key in depth[i].keys():
            if i!=d:
                #print key
                if depth_values[i][key][3]!=-1:
                    if depth_values[i][key][3]==total_count[key] and (isinstance(depth_values[i][key][1], int) or isinstance(depth_values[i][key][2], int)):
                        depth_values[i][key][3]-=1
                        #printStatements(key, i, depth_values[i][key][0], depth_values[i][key][1], depth_values[i][key][2])
                        for key1 in depth_values[i+1].keys():
                            depth_values[i+1][key1][1] = depth_values[i][key][1]
                            depth_values[i+1][key1][2] = depth_values[i][key][2]
                        i+=1
                        break
                    if i%2==0: # max
                        depth_values[i][key][0] = max(x, depth_values[i][key][0])
                        if depth_values[i][key][0]>= depth_values[i][key][2]:
                            depth_values[i][key][3] = -1
                            x=depth_values[i][key][0]
                            #printStatements(key, i, depth_values[i][key][0], depth_values[i][key][1], depth_values[i][key][2])
                            for key3 in depth_values[i+1].keys():
                                if key3.startswith(key):
                                    depth_values[i+1][key3][3] = -1
                            i-=1
                            break
                        else:
                            depth_values[i][key][1] = max(depth_values[i][key][0],depth_values[i][key][1])
                    else: # min
                        depth_values[i][key][0] = min(x, depth_values[i][key][0])
                        if depth_values[i][key][0]<= depth_values[i][key][1]:
                            depth_values[i][key][3] = -1
                            x=depth_values[i][key][0]
                            #printStatements(key, i, depth_values[i][key][0], depth_values[i][key][1], depth_values[i][key][2])
                            for key3 in depth_values[i+1].keys():
                                if key3.startswith(key):
                                    depth_values[i+1][key3][3] = -1
                            i-=1
                            break
                        else:
                            depth_values[i][key][2] = min(depth_values[i][key][0],depth_values[i][key][2])
                    depth_values[i][key][3]-=1
                    #printStatements(key, i, depth_values[i][key][0], depth_values[i][key][1], depth_values[i][key][2])
                    for key2 in depth[i+1].keys():
                        if key2.startswith(key):
                            if depth_values[i+1][key2][3]>=0:
                                depth_values[i+1][key2][1] = depth_values[i][key][1]
                                depth_values[i+1][key2][2] = depth_values[i][key][2]
                    if depth_values[i][key][3]==-1:
                        x=depth_values[i][key][0]
                        i-=1
                        break
                else: # for key already read
                    continue
                i+=1
                #print i
                break
            else:
                if depth_values[i][key][3]==0:
                    depth_values[i][key][3]=-1
                    #printStatements(key, i, depth_values[i][key][0], depth_values[i][key][1], depth_values[i][key][2])
                    x = depth_values[i][key][0]
                    #print i, "=i in ="
                    i-=1
                    break
    return
            
            
def alphabetaPrint():
    #for who = X
    # initial parsing till terminal node
    i=0
    p=1
    for i in range(d):
        p=1
        for key in depth_values[i].keys():
            if p==1:
                p=0
                depth_values[i][key][3]-=1
                printStatements(key, i, depth_values[i][key][0], depth_values[i][key][1], depth_values[i][key][2])
    i+=1        
    while depth_values[0]['root'][3]>=-1 and i>=0:
        #count-=1
        for key in depth[i].keys():
            if i!=d:
                #print key
                if depth_values[i][key][3]!=-1:
                    if depth_values[i][key][3]==total_count[key] and (isinstance(depth_values[i][key][1], int) or isinstance(depth_values[i][key][2], int)):
                        depth_values[i][key][3]-=1
                        printStatements(key, i, depth_values[i][key][0], depth_values[i][key][1], depth_values[i][key][2])
                        for key1 in depth_values[i+1].keys():
                            depth_values[i+1][key1][1] = depth_values[i][key][1]
                            depth_values[i+1][key1][2] = depth_values[i][key][2]
                        i+=1
                        break
                    if i%2==0: # max
                        depth_values[i][key][0] = max(x, depth_values[i][key][0])
                        if depth_values[i][key][0]>= depth_values[i][key][2]:
                            depth_values[i][key][3] = -1
                            x=depth_values[i][key][0]
                            printStatements(key, i, depth_values[i][key][0], depth_values[i][key][1], depth_values[i][key][2])
                            for key3 in depth_values[i+1].keys():
                                if key3.startswith(key):
                                    depth_values[i+1][key3][3] = -1
                            i-=1
                            break
                        else:
                            depth_values[i][key][1] = max(depth_values[i][key][0],depth_values[i][key][1])
                    else: # min
                        depth_values[i][key][0] = min(x, depth_values[i][key][0])
                        if depth_values[i][key][0]<= depth_values[i][key][1]:
                            depth_values[i][key][3] = -1
                            x=depth_values[i][key][0]
                            printStatements(key, i, depth_values[i][key][0], depth_values[i][key][1], depth_values[i][key][2])
                            for key3 in depth_values[i+1].keys():
                                if key3.startswith(key):
                                    depth_values[i+1][key3][3] = -1
                            i-=1
                            break
                        else:
                            depth_values[i][key][2] = min(depth_values[i][key][0],depth_values[i][key][2])
                    depth_values[i][key][3]-=1
                    printStatements(key, i, depth_values[i][key][0], depth_values[i][key][1], depth_values[i][key][2])
                    for key2 in depth[i+1].keys():
                        if key2.startswith(key):
                            if depth_values[i+1][key2][3]>=0:
                                depth_values[i+1][key2][1] = depth_values[i][key][1]
                                depth_values[i+1][key2][2] = depth_values[i][key][2]
                    if depth_values[i][key][3]==-1:
                        x=depth_values[i][key][0]
                        i-=1
                        break
                else: # for key already read
                    continue
                i+=1
                #print i
                break
            else:
                if depth_values[i][key][3]==0:
                    depth_values[i][key][3]=-1
                    printStatements(key, i, depth_values[i][key][0], depth_values[i][key][1], depth_values[i][key][2])
                    x = depth_values[i][key][0]
                    #print i, "=i in ="
                    i-=1
                    break
    return

if __name__ == '__main__':
    #global nextNodes
    #global nextNums
    #global elem
    #global d
    if who == 'X':
        chance = 0
    else:
        chance = 1
    for i in range(d):
        depth[i+1] = OrderedDict()
        if chance == 0:
            #print "X turn"
            for key in depth[i].keys():
                searchXPos(depth[i][key])
                if len(nextNodes) == 0:
                    depth[i+1].update(OrderedDict([(key+'-pass', depth[i][key])]))
                else:
                    depth[i+1].update(OrderedDict((key+"-"+a, 0) for a in nextNodes))                   
                    val = key+"-"
                    changeO(val, i+1, depth[i][key])
                #printGrid(depth[i][key])
                nextNums = []
                nextNodes = []
                elem = []
            chance = 1
        else:
            #print "O turn"
            for key in depth[i].keys():
                searchOPos(depth[i][key])
                if len(nextNodes) == 0:
                    depth[i+1].update(OrderedDict([(key+'-pass', depth[i][key])]))
                else:
                    depth[i+1].update(OrderedDict((key+"-"+a, 0) for a in nextNodes))
                    val = key+"-"
                    changeX(val, i+1, depth[i][key])
                #printGrid(depth[i][key])
                nextNums = []
                nextNodes = []
                elem = []
            chance = 0

    for i in range(d):
        if i>0:
            if len(depth[i])==1 and len(depth[i+1])==1 and depth[i+1].items()[0][0].endswith('pass-pass'):
                d = i+1
                break

    getTotalValues()
    updateDepthValues()
    alphabeta()


    for key in depth[d].keys():
        if depth_values[d][key][0]==depth_values[0]['root'][1]:
            key_name = key.split('-',2)[0]+"-"+key.split('-',2)[1]
            printGrid(depth[1][key_name])
            break

    updateDepthValues()
    alphabetaPrint()
    op.close()
                

                


