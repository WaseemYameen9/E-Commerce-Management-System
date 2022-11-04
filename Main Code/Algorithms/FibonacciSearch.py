# import pandas as pd
# import ShellSort2

#        ------Searching With Filters-------------


def wordStartWith(firstLetter, comparisonLetter):
    firstLetter = list(firstLetter)
    comparisonLetter = list(comparisonLetter)
    for i in range(len(comparisonLetter)):
        if (comparisonLetter[i] != firstLetter[i]):
            return False
    return True

def wordExactEquals(firstLetter,comparisonLetter):
    if firstLetter == comparisonLetter:
        return True
    else:
        return False
    
def wordEndWith(firstLetter, comparisonLetter):
    firstLetter = list(firstLetter)
    comparisonLetter = list(comparisonLetter)
    firstLetter = firstLetter[::-1]
    comparisonLetter = comparisonLetter[::-1]
    for i in range(len(comparisonLetter)):
        if (comparisonLetter[i] != firstLetter[i]):
            return False
    return True

def wordContains(firstLetter, comparisonLetter):
    if comparisonLetter in firstLetter:
        return True
    return False

def compareBySwitchingCondition(firstLetter,comparisonLetter,switchingNo):
    if(switchingNo == 0): # start With
        return wordStartWith(firstLetter,comparisonLetter)
    if(switchingNo == 1): # End With
        return wordEndWith(firstLetter,comparisonLetter)
    if(switchingNo == 2): # Contains With
        return wordContains(firstLetter,comparisonLetter)
    if(switchingNo == 3): # Exact With
        return wordExactEquals(firstLetter,comparisonLetter)
    return False

#-----------------------Generates Fibonacci Numbers-----------------------------
def GenerateNumbers(n):
    if n < 1:
        return 0
    elif n == 1:
        return 1
    else:
        return GenerateNumbers(n - 1) + GenerateNumbers(n - 2)
    
#-----------------------Searches From next half of array----------------------------
def FibonacciSearch_Forward(A, req,FilterNum):
    m = 0 
    while GenerateNumbers(m) < len(A): # 
        m = m + 1 
    offset = -1
    while (GenerateNumbers(m) > 1):

        i = min( offset + GenerateNumbers(m - 2) , len(A) - 1)
        if compareBySwitchingCondition(str(A[i]), req, FilterNum):
            return i
            
        elif (req < A[i]):
            m = m - 2
        elif (req > A[i]):
            m = m - 1
            offset = i
        # if(A[offset + 1] == req):
        #     return offset + 1
    return None

#----------------------Searches From First half of array-----------------------------
def FibonacciSearch_Backward(A, req,FilterNum):
    m = 0 
    while GenerateNumbers(m) < len(A): # 
        m = m + 1 
    offset = -1
    while (GenerateNumbers(m) > 1):

        i = min( offset + GenerateNumbers(m - 2) , len(A) - 1)
        if compareBySwitchingCondition(str(A[i]), req, FilterNum):
            return i
        elif (req < A[i]):
            m = m - 2
        elif (req > A[i]):
            m = m - 1
            # offset = i
    return None

#---------------------Returns Next Half serached index from array-----------------------
def Forward_forStrings(Arr,Required,FilterNum):
    Temp = Arr[:]
    ind =[]
    # offset = 0
    # idx = 0
    # Finalidx = []
    for i in range(len(Temp)):
        try:
            a = FibonacciSearch_Forward(Temp, Required,FilterNum)
        except:
            a = None
        if a != None:
            Temp[a] = ' '
            ind.append(a)
        else:
            break
    return ind

#--------------------Returns First Half serached index from array-----------------------
def Backward_forStrings(Arr,Required,FilterNum):
    Temp = Arr[:]
    ind =[]
    # offset = 0
    # idx = 0
    # Finalidx = []
    for i in range(len(Temp)):
        try:
            a = FibonacciSearch_Backward(Temp, Required,FilterNum)
        except:
            a = None
        if a != None:
            Temp[a] = ' '
            ind.append(a)
        else:
            break
    return ind

#--------------------Change indexes to Arrays---------------------------------
def ChangeIdxToArray(List,mainList):
    List = list(List)
    arr = [[0 for i in range(len(List))] for j in range(7)]
    for i in range(len(List)):
        arr[0][i] = mainList[0][List[i]]
        arr[1][i] = mainList[1][List[i]]
        arr[2][i] = mainList[2][List[i]]
        arr[3][i] = mainList[3][List[i]]
        arr[4][i] = mainList[4][List[i]]
        arr[5][i] = mainList[5][List[i]]
        arr[6][i] = mainList[6][List[i]]
    return arr,List

#------------------Main Function to call, it return searched array and it's indexes-------------------
def MainFuncforFibnacci(Arr,rownumber,Required,FilterNum):
    lis = []
    for i in range(0,len(Arr[rownumber])-200,200):
        first = Backward_forStrings((Arr[rownumber])[i: 200 + i], Required,FilterNum)
        second = Forward_forStrings((Arr[rownumber])[i: 200 + i], Required,FilterNum)
        if i>0:    
            for idx in range(len(first)):
                if first:
                    first[idx] = first[idx] + i
            for idx in range(len(second)):
                if second:
                    second[idx] = second[idx] + i
        for i in first:
            lis.append(i)
        for a in second:
            lis.append(a)
    lis = set(lis)
    return ChangeIdxToArray(lis,Arr)


    
# mainList = []
# df = pd.read_csv('C:\\DSA\\Python Files\\CombineData.csv')
# for t in range(1,8):
#     List = []
#     for p in range(0,5000):
#         List.append(df.iloc[p,t])
#     mainList.append(List)
# ShellSort2.ShellSort_Asc(mainList, 0)
# l = MainFuncforFibnacci(mainList,0,'e',1)