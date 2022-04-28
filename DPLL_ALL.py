import sys, copy, time
sys.setrecursionlimit(10000)

def readInput(stri):
    f_path="C:\\Users\\abhip\OneDrive\Desktop\CODE\VSC code\CS202\Ass2\\testcases\\"
    inputFile = open(f_path+stri+".cnf",'r')    
    clause_strs = inputFile.read().split('\n')
    j = 0
    x = []
    for s in clause_strs:
        literals = s.split()
        y = []
        for lit in literals:
            if(j == 1):
                y.append(int(lit))
                if variables[abs(int(lit))-1] == 0:
                    variables[abs(int(lit))-1] = 1 #shows the presence in x
            if lit == 'p':
                n,l = int(literals[2]),int(literals[3])
                j = 1
                variables = [0 for i in range(n)]
                break;
        if len(y) != 0:
            y.pop()
            x.append(y)
    return x,n,l,variables

def maximumOccurence(x,n):
    pos = [0 for i in range(n)]
    both = [0 for i in range(n)]
    y = 0
    for lines in x:
        for lit in lines:
            both[abs(lit)-1] += 1
            y = abs(lit) if both[abs(lit)-1] > both[abs(y)-1] else abs(y)
            if(lit > 0):
                pos[abs(lit)-1] +=1
    return y if 2*pos[abs(y)-1] >= both[abs(y)-1] else -y

def DPLL(y,num,model):
    global finalModel
    x = copy.deepcopy(y)
    #------------------unit propagate--------------------------------
    while(1):
        if len(x) == 0:
            finalModel=model
            return True
        sign = [0 for i in range(num)]
        hasUnitClause = 0
        for lines in x:
            if len(lines) == 1:
                hasUnitClause = 1
                if sign[abs(lines[0])-1] == 0:
                    sign[abs(lines[0])-1] = 1 if (lines[0]>0) else -1
                    model[abs(lines[0])-1]=lines[0]
                    x.remove(lines)
                    i=0
                    length=len(x)
                    while(i<length):
                        if lines[0] in x[i]:
                            x.remove(x[i])
                            length-=1
                        elif -lines[0] in x[i]:
                            x[i].remove(-lines[0])
                            i+=1    
                        else :
                            i+=1                        
                else:
                    if (int (lines[0])/abs(lines[0]) + sign[abs(lines[0])-1]==0):
                        return False
        if hasUnitClause == 0:
            break
    #---------------------X is empty-----------------------------------
    if len(x) == 0:
        finalModel = copy.deepcopy(model)
        return True
    #---------------------Empty clause----------------------------------
    for lines in x:
        if len(lines) == 0:
            return False
    #--------------------pure literal case-----------------------------
    diffSign = [-1 for i in range(num)]
        #-1=>nothing, 0=>negative, 1=>positive, 2=>sign changes
    for lines in x:
        for lit in lines:
            if diffSign[abs(lit)-1] == -1:
                diffSign[abs(lit)-1] = (lit>0)
            else:
                if diffSign[abs(lit)-1] != (lit>0):
                    diffSign[abs(lit)-1] = 2
    for lines in x:
        for lit in lines:
            if diffSign[abs(lit)-1] ==1 or diffSign[abs(lit)-1] == 0:
                model[abs(lit)-1]=lit
                i =0
                length=len(x)
                while(i<length):
                    if lit in x[i]:
                        x.remove(x[i])
                        length-=1
                    elif -lit in x[i]:
                        x[i].remove(lit)
                        i+=1
                    else:
                        i+=1
    #---------------------X is empty-----------------------------------
    if len(x) == 0:
        finalModel = copy.deepcopy(model)
        return True
    #---------------------Empty clause----------------------------------
    for lines in x:
        if len(lines) == 0:
            return False
    #---------------------recursive DPLL---------------------------------
    i = maximumOccurence(x,num)
    return DPLL(x+[[i]], num, list(model)) or DPLL(x+[[-i]], num, list(model))
filenames=["uf20-0","uf150-0","uuf150"]
for file in filenames:
    t = time.time()
    if file==filenames[2]:
        numb=20
    else:
        numb=15
    for i in range(1,numb+1):
        inputLines, number, numLines, variables = readInput(file+str(i))
        finalModel = [i+1 for i in range(number)]
        print("\n{0}{1}{2}     |".format(file,str(i),".cnf"),end="")
        if DPLL(inputLines, number, finalModel):
            print("\t SAT ","|\tTime taken:" ,time.time()-t,"seconds")
            print(finalModel)
        else:
            print("\tUNSAT\n")
        print("___________________________________________________________________________________________________________________________________________________________________________")
