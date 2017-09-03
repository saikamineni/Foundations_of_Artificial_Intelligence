import itertools
from decimal import Decimal, ROUND_HALF_UP
file_c1 = []
with open("input.txt") as f:
    for line in f:
        line = line.replace("\n", "").replace("\r", "")
        file_c1.append(line)
file_c2 = file_c1

to_calc = {}
truth_ts = {}
final_vals = {}
dec = [] # decision variables
utility = {}
loc1 = file_c1.index("******")
for count in range(1, loc1+1):
    to_calc[count] = file_c1[count-1].replace(" ", "").replace("=","")
file_c1 = file_c1[loc1+1:]


count = file_c1.count("***")+1
while count!=0:
    if count > 1:
        loc1 = file_c1.index("***")
    else:
        loc1 = 0

    if loc1 == 2:
        if file_c1[1] == 'decision':
            dec.append(file_c1[0])
        else:
            truth_ts[file_c1[0]] = {"+":file_c1[1]}
    else:
        l1 = file_c1[0].split(" ")
        eles = len(l1)-2
        vals = {}
        for i in range(1, (2**eles)+1):
            #print file_c1[i]
            file_c1[i] = file_c1[i].replace(" ", "")
            vals[file_c1[i][-eles:]] = file_c1[i][:-eles]
        truth_ts[file_c1[0]] = vals
    if count == 1:
        if file_c1.count("******") == 1:
            file_c1 = file_c1[file_c1.index("******")+1:]
        else:
            file_c1 = []
    else:
        file_c1 = file_c1[loc1+1:]
    count = count - 1


if len(file_c1)>0:
    file_c1[0] = file_c1[0].replace("utility | ", "")
    l1 = file_c1[0].split(" ")
    eles = len(l1)
    vals = {}
    for i in range(1, (2**eles)+1):
        file_c1[i] = file_c1[i].replace(" ", "")
        vals[file_c1[i][-eles:]] = file_c1[i][:-eles]
    utility[file_c1[0]] = vals
    file_c1 = []


depend = {}
for key in truth_ts:
    if key.find('|') != -1:
        depend[key[:key.find('|')-1]] = key[key.find('|')+1:].split(" ")
        depend[key[:key.find('|')-1]].remove("")
    else:
        depend[key] = []
for ele in dec:
    depend[ele] = []



#all_vars = []
def decompose(var):
    if var[-1] == "+" or var[-1] == '-':
        all_vars1 = [var[:-1]]
    else:
        all_vars1 = [var]
    for ele in all_vars1:
        if ele not in dec:
            all_vars1.extend(depend[ele])
    all_vars1 = list(set(all_vars1))
    return all_vars1


def sortCl1(p):
    new = []
    p = list(reversed(p))
    for i in range(0, len(p)):
        for j in range(i+1, len(p)):
            if p[i] in decompose(p[j]):
                continue
            elif p[j] in decompose(p[i]):
                t = p[i]
                p[i] = p[j]
                p[j] = t
            else:
                continue
    return p


def sortCl(p):
    new = []
    p = list(reversed(p))
    for i in range(0, len(p)):
        for j in range(i+1, len(p)):
            if p[i][:-1] in decompose(p[j]):
                continue
            elif p[j][:-1] in decompose(p[i]):
                t = p[i]
                p[i] = p[j]
                p[j] = t
            else:
                continue
    return p

given = []
all_vars_vals = {}
done = []

def calcAll(given, all_vars):
    global all_vars_vals
    #global given
    #global all_vars
    indep = []
    given1 = []
    for keys in depend:
        if len(depend[keys]) == 0:
            indep.append(keys)
    all_vars_vals = {}
    for ele in list(set(all_vars+indep)):
        all_vars_vals[ele+'+'] = None
        all_vars_vals[ele+'-'] = None
    for ele in given:
        all_vars_vals[ele] = 1
        if ele[-1] == '+':
            all_vars_vals[ele[:-1]+'-'] = 0
        else:
            all_vars_vals[ele[:-1]+'+'] = 0
    for keys in total_vars:
        if total_vars[keys] is not None and keys in all_vars_vals.keys():
            all_vars_vals[keys] = total_vars[keys]
    for ele in indep:
        if all_vars_vals[ele+'+'] is None:
            if ele in dec:
                all_vars_vals[ele+'+'] = 1
                all_vars_vals[ele+'-'] = 1
            else:
                all_vars_vals[ele+'+'] = float(truth_ts[ele]['+'])
                all_vars_vals[ele+'-'] = 1 - float(truth_ts[ele]['+'])
    for giv in given:
        given1.append(giv[:-1])
    all_vars = sortCl1(all_vars)
    #print "all_vars", all_vars
    #print all_vars_vals
    while (None in all_vars_vals.values()):
        for ele in all_vars:
            if all_vars_vals[ele+'+'] is None:
                if set(depend[ele]) <= set(indep+given1):
                    sum_all = 0
                    all_need = list([e1+'+', e1+'-'] for e1 in depend[ele])
                    cp_all = list(itertools.product(*all_need))
                    for elem in cp_all:
                        prod = 1
                        for item in elem:
                            prod = prod*float(all_vars_vals[item])
                        #print "prod*float(all_vars_vals[item])", prod,float(truth_ts[ele+' | '+" ".join(w[:-1] for w in elem)]["".join(w[-1] for w in elem)])
                        prod = prod*float(truth_ts[ele+' | '+" ".join(w[:-1] for w in elem)]["".join(w[-1] for w in elem)])
                        sum_all = sum_all + prod
                    all_vars_vals[ele+'+'] = sum_all
                    #print "all_vars_vals", ele+'+', sum_all
                    all_vars_vals[ele+'-'] = 1 - sum_all
                    indep.append(ele)
                else:
                    continue
                
def causalUpdate(ele):
    #global given
    global done
    new = []
    for elem in decompose(ele[:-1]):
        if depend[elem] == []:
            new.append(elem)
    for item in new:
        all_vars = decompose(ele)
        calcAll([], all_vars)
        c = all_vars_vals[ele]
        #c = calPValue('P('+ele+')')
        all_vars = decompose(ele)
        calcAll([item+'+'], all_vars)
        a = all_vars_vals[ele]
        #a = calPValue('P('+ele+'|'+item+'+)')
        all_vars = decompose(item+'+')
        calcAll([], all_vars)
        b = all_vars_vals[item+'+']
        #b = calPValue('P('+item+'+)')
        done.append(ele)
        total_vars[item+'+'] = (a*b)/c
        total_vars[item+'-'] = 1- total_vars[item+'+']
        #print "in Causal",item+'+', total_vars[item+'+']
    #print "done", done


def calPValue(clause):
    #print clause
    #global all_vars
    global given
    total = 1
    given = []
    if clause.find('|') != -1 :
        given = given + clause[clause.find('|')+1:-1].split(',')
        #print "given", given, done
        for el in given:
            if len(depend[el[:-1]]) != 0 and el not in done:
                #print "to Causal", el
                causalUpdate(el)
        for item in sortCl(clause[2:clause.find('|')].split(',')):
            #print "item", item
            all_vars = decompose(item)
            calcAll(given, all_vars)
            total = total * all_vars_vals[item]
            '''
            #print "total", all_vars_vals[item]
            #print "all_vars_vals", all_vars_vals
            if item not in done:
                causalUpdate(item)
            '''
            given.append(item)
        final_vals[key] = total
    else:
        for item in sortCl(clause[2:-1].split(',')):
            #print "item", item
            all_vars = decompose(item)
            calcAll(given, all_vars)
            total = total * all_vars_vals[item]
            '''
            #print "total", all_vars_vals[item]
            #print "all_vars_vals", all_vars_vals
            if item not in done:
                causalUpdate(item)
            '''
            given.append(item)
    return total


def calUValue(clause):
    #print clause
    global given
    eu_vars = {}
    given = []
    sum_all = 0
    given = given + clause[3:-1].replace("|", ",").split(",")
    #print given
    items = utility.keys()[0].split(" ")
    #print "utility items", items
    for item in items:
        if item+"+" in given or item+'-' in given:
            items.remove(item)
    all_need = list(e1+'+' for e1 in items)
    all_need = sortCl(all_need)
    #print "all_need", all_need
    for item in all_need:
        all_vars = decompose(item)
        calcAll(given, all_vars)
        given.append(item)
        for keys in all_vars_vals:
            if keys not in eu_vars:
                eu_vars[keys] = all_vars_vals[keys]
        #print item
            #print eu_vars
    items = utility.keys()[0].split(" ")
    all_need = list([e1+'+', e1+'-'] for e1 in items)
    cp_all = list(itertools.product(*all_need))
    for ele in cp_all:
        prod = 1
        for item in ele:
            prod = prod * float(eu_vars[item])
        sum_all = sum_all + (prod * float(utility.values()[0]["".join(w[-1] for w in ele)]))
    return sum_all

for key in to_calc:
    #key = 5
    done = []
    total_vars = {}
    for keys in depend:
        total_vars[keys+'+'] = None
        total_vars[keys+'-'] = None
    given = []
    if to_calc[key][0] == 'P':
        final_vals[key] = calPValue(to_calc[key])
        #print final_vals[key]
        final_vals[key] = "%.2f" %float((Decimal(final_vals[key]+0.000000001).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)))
    elif to_calc[key][0] == 'E':
        eu_vars = {}
        final_vals[key] = calUValue(to_calc[key])
        final_vals[key] = int(round(final_vals[key], 0))
    elif to_calc[key][0] == 'M':
        max_utils = {}
        if to_calc[key][4:-1].find('|') == -1:
            all_need = list([e1+'+', e1+'-'] for e1 in to_calc[key][4:-1].split(","))
            cp_all = list(itertools.product(*all_need))
            for i in cp_all:
                symbols = ''
                clause = "EU("
                for j in i:
                    symbols = symbols + j[-1]
                    clause = clause + j + ","
                clause = clause[:-1]
                clause = clause +")"
                #print clause
                max_utils[symbols] = calUValue(clause)
                max_utils[symbols] = int(round(max_utils[symbols], 0))
        else:
            pos = to_calc[key].find("|")
            all_need = list([e1+'+', e1+'-'] for e1 in to_calc[key][4:pos].split(","))
            cp_all = list(itertools.product(*all_need))
            for i in cp_all:
                symbols = ''
                clause = "EU("
                for j in i:
                    symbols = symbols + j[-1]
                    clause = clause + j + ","
                clause = clause[:-1]
                clause = clause +to_calc[key][pos:-1] + ")"
                #print clause
                #print symbols
                max_utils[symbols] = calUValue(clause)
                max_utils[symbols] = int(round(max_utils[symbols], 0))
        #print max_utils
        for keys in max_utils:
            if max_utils[keys] == max(max_utils.values()):
                final_vals[key] = " ".join(list(keys)) + " " + str(max_utils[keys])
            
    #break

op = open("output.txt", 'w')
for i in final_vals:
    op.write(str(final_vals[i])+"\n")

op.close()
