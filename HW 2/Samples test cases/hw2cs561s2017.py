import copy
import random

init_clauses = {}
clauses_assign = {}
literals_sat = {}
literal_assign = {}
clauses = {}
persons = []
literals = {}
clauses_values = {}
literals_new = {}
satis = 3
def createClauses(M, N, reqd):
    global literals
    for i in range(M): # traverse through persons
        if i+1 in reqd:
            cl1 = {}
            for j in range(N): # traverse through tables
                cl1[i+1,j+1]='X'
                for k in range(j+1,N+1):
                    if (k<N): # case for 2 tables
                        clauses[hash(frozenset({(i+1,j+1):'Y', (i+1, k+1):'Y'}.items()))] = {(i+1,j+1):'Y', (i+1, k+1):'Y'}
                        clauses_values[hash(frozenset({(i+1,j+1):'Y', (i+1, k+1):'Y'}.items()))] = 0
            clauses[hash(frozenset(cl1.items()))] = cl1
            clauses_values[hash(frozenset(cl1.items()))] = 0
    return


def friendsClauses(a, b):
    for i in range(N):
        #cl1 = {}
        #for j in range(N): # can't sit on different tables
            #if i!=j:
                #cl1[int(a), i+1] = 'Y'#.append(bytearray('Y-'+str(a)+'-'+str(i+1)))
                #cl1[int(b), j+1] = 'Y'
            
        cl2 = {}
        cl2[int(a), i+1] = 'Y'#.append(bytearray('Y-'+str(a)+'-'+str(i+1)))
        cl2[int(b), i+1] = 'X'#.append(bytearray('X-'+str(b)+'-'+str(i+1)))
        #clauses.append(cl2)
        clauses[hash(frozenset(cl2.items()))] = cl2
        clauses_values[hash(frozenset(cl2.items()))] = 0
        cl2 = {}
        cl2[int(a), i+1] = 'X'#.append(bytearray('X-'+str(a)+'-'+str(i+1)))
        cl2[int(b), i+1] = 'Y'#.append(bytearray('Y-'+str(b)+'-'+str(i+1)))
        #clauses.append(cl2)
        clauses[hash(frozenset(cl2.items()))] = cl2
        clauses_values[hash(frozenset(cl2.items()))] = 0
    return

def enemiesCluases(a, b):
    for i in range(N):
        cl1 = {}
        cl1[int(a), i+1] = 'Y'#.append(bytearray('Y-'+str(a)+'-'+str(i+1)))
        cl1[int(b), i+1] = 'Y'#.append(bytearray('Y-'+str(b)+'-'+str(i+1)))
        #clauses.append(cl1)
        clauses[hash(frozenset(cl1.items()))] = cl1
        clauses_values[hash(frozenset(cl1.items()))] = 0
    return

def extract_literals():
    global literals_new
    literals_new = {}
    for key in clauses.keys():
        for key1 in clauses[key].keys():
            literals_new[key1, clauses[key][key1]] = 0


count = 0
with open("input.txt") as f:
    for line in f:
        x=line.split(' ')
        if count == 0:
            count = count + 1
            M = int(x[0])
            N = int(x[1])
            #print len(clauses)
        else:
            if x[2][0] == 'F':
                persons.append(int(x[0]))
                persons.append(int(x[1]))
                #print x[0], x[1]
                friendsClauses(x[0], x[1])
            elif x[2][0] == 'E':
                persons.append(int(x[0]))
                persons.append(int(x[1]))
                #print x[0], x[1]
                enemiesCluases(x[0], x[1])
    createClauses(M, N, list(set(persons)))

f.close()
extract_literals()
literals = copy.deepcopy(literals_new)
init_clauses = copy.deepcopy(clauses)
for key in literals.keys():
    literals_sat[hash(frozenset({key[0]: key[1]}))] = {key[0]: key[1]}

for i in range(M):
    for j in range(N):
        literals_sat[hash(frozenset({(i+1,j+1):'X'}))] = {(i+1,j+1):'X'}


def findPureSymbol():
    found = False
    all_keys = []
    for key in literals_new.keys():
        all_keys.append(key[0])
    
        
    for x in all_keys:
        if all_keys.count(x) == 1:
            found = True
            break

    if found:
        for key in literals_new.keys():
            if key[0] == x:
                value = key[1]
                break
        literals[x, value] = 1
        for k1, val in clauses.items(): # all the clauses
            for pos, v1 in val.items(): # getting positions
                if x == pos:# and 
                    clauses_values[k1] = 1
                    clauses[k1] = {}
        return True
    return False

def findUnitClause():
    found = False
    for value in clauses.values():
        if len(value) == 1:
            found = True
            break

    if found:
        literals[value.keys()[0], value.values()[0]] = 1
        for k1, val in clauses.items(): # all the clauses
            for pos, v1 in val.items(): # getting positions
                if value.keys()[0] == pos:# and 
                    if value.values()[0] == v1: # checking for position
                        clauses_values[k1] = 1
                        clauses[k1] = {}#.pop(value.keys()[0], value.keys()[0])
                    else:
                        clauses[k1].pop(pos, v1)
                        if len(clauses[k1]) == 0:
                            clauses_values[k1] = -1
                        literals[value.keys()[0], v1] = -1
        #print "Clauses", clauses
        #extract_literals()
        return True
    return False

def DPLL():
    global satis
    if set(clauses_values.values()) == {1}:
        satis = True
        return 
    elif -1 in clauses_values.values():
        satis = False
        return 
    extract_literals()
    if not findPureSymbol():
        extract_literals()
        if not findUnitClause():
            if len(literals_new) > 0:
                literals[literals_new.keys()[0]] = 1
                for k1, val in clauses.items():
                    for pos, v1 in val.items():
                        if literals_new.keys()[0][0] == pos:
                            if literals_new.keys()[0][1] == v1:
                                clauses_values[k1] = 1
                                clauses[k1] = {}
                            else:
                                clauses[k1].pop(pos, v1)
                                literals[literals_new.keys()[0][0], v1] = -1
    DPLL()
    return


def randomAssignment():
    global literal_assign
    for i in literals_sat.keys():
        literal_assign[i] = random.randint(0,1)

clauses_temp = {}
def generateModel(literal_given):
    for i in init_clauses.keys():
        vals = []
        for key in init_clauses[i].keys():
            if init_clauses[i][key] == 'X':
                vals.append(literal_given[hash(frozenset({key:'X'}))])
            else:
                if literal_given[hash(frozenset({key:'X'}))] == 0:
                    vals.append(1)
                else:
                    vals.append(0)
        if 1 in vals:
            clauses_temp[i] = 1
        else:
            clauses_temp[i] = 0
    return clauses_temp

def flipGiven(val):
    global clauses_assign
    global literal_assign
    temp_literals = literal_assign
    if temp_literals[val] == 0:
        temp_literals[val] = 1
    else:
        temp_literals[val] = 0
    clauses_temp = generateModel(temp_literals)
    literal_assign = temp_literals
    clauses_assign = clauses_temp
    return

def flipFind(vals):
    global clauses_assign
    global literal_assign
    temp_literals = literal_assign
    pos = {}
    max_difference = len({k: v for k, v in clauses_assign.items() if v==0})
    for val in vals:
        temp_literals = literal_assign
        if temp_literals[hash(frozenset({val:'X'}))] == 0:
            temp_literals[hash(frozenset({val:'X'}))] = 1
        else:
            temp_literals[hash(frozenset({val:'X'}))] = 0
        clauses_temp = generateModel(temp_literals)
        if max_difference<=len({k: v for k, v in clauses_temp.items() if v==0}):
            continue
        else:
            pos[len({k: v for k, v in clauses_temp.items() if v==0})] = val
            max_difference = len({k: v for k, v in clauses_temp.items() if v==0})
    
    if len(pos) == 0:
        return
    if literal_assign[hash(frozenset({pos[max_difference]:'X'}))] == 0:
        literal_assign[hash(frozenset({pos[max_difference]}))] = 1
    else:
        literal_assign[hash(frozenset({pos[max_difference]}))] = 0

    clauses_assign = generateModel(literal_assign)
    return

#maxFlips = 100
p = 0.5
def walkSAT():
    global clauses_assign
    randomAssignment()
    clauses_assign = generateModel(literal_assign)
    while(1):
        if set(clauses_assign.values()) == {1}:
            return True
        selected = init_clauses[random.choice({k: v for k, v in clauses_assign.items() if v==0}.keys())]
        if random.uniform(0,1)<p:
            k = random.choice(selected.keys())
            flipGiven(hash(frozenset({k:'X'})))
        else:
            flipFind(selected.keys())
        
        
        
DPLL()
op = open("output.txt", 'w')
if satis:
    op.write("yes\n")
    #print "yes"
    if (walkSAT()):
        arrange = {}
        for i in literal_assign.keys():
            if literal_assign[i] == 1:
                a, b = literals_sat[i].keys()[0]
                arrange[a] = b
        for i in arrange.keys():
            #print i, arrange[i]
            op.write(str(i)+" "+str(arrange[i])+"\n")
else:
    #print "no"
    op.write("no")

op.close()


