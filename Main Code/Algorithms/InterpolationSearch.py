import math
# import pandas as pd
# import ShellSort2
#-----------------------------------Gets Matching First Caharcter Index-------------------------------------
def interpolation_search_forStrings(A, key):
    low = 0
    high = len(A) - 1
    while ord((A[low])[0]) <= ord(key) <= ord((A[high])[0]) and ord((A[high])[0]) != ord((A[low])[0]):
        #  FInds the closest or exact position of the element
        position = math.floor(low + (ord(key) - ord((A[low])[0])) * (high - low) / (ord((A[high])[0]) - (ord((A[low])[0]))))
        if ord((A[position])[0]) == ord(key):
            return position
        elif ord((A[position])[0]) > ord(key):
            high = position - 1
        else:
            low = position + 1
    if ord(key) == ord((A[low])[0]):
        return low
    return None
#-----------------------------------Returns All the index Starting with Required Character--------------------
def forString(Arr,rownumber,Required):
    Arr = Arr[rownumber]
    ind =[]
    offset = 0
    for i in range(len(Arr)):
        try:
            a = interpolation_search_forStrings(Arr[offset:], Required)
        except:
            a = None
        if a != None:
            if i == 0:
                actual = a
                offset = a
            ind.append(actual)
            offset += 1
            actual += 1
        else:
            break
    return ind
#-----------------------------------Gets Matching Number's Index--------------------------------
def interpolation_search_forNumbers(A, key):
    low = 0
    high = len(A) - 1
    key = math.floor(key)
    while math.floor(A[low])<= key <= math.floor(A[high]) and math.floor(A[high]) != math.floor(A[low]):
        #  FInds the closest or exact position of the element
        position = math.floor(low + ((key - math.floor(A[low])) * (high - low) / (math.floor(A[high]) - math.floor(A[low]))))
        if math.floor(A[position]) == key:
            return position
        elif math.floor(A[position]) > key:
            high = position - 1
        else:
            low = position + 1
    if key == math.floor(A[low]):
        return low
    return None
#-----------------------------------Returns All the index for Required Integers or Floats------------------
def forNumbers(Arr,rownumber,Required):
    Arr = Arr[rownumber]
    ind =[]
    offset = 0
    if(rownumber == 6):
        Required *= 10
        for i in range(len(Arr)):
            Arr[i] = Arr[i] * 10
    for i in range(len(Arr)):
        try:
            a = interpolation_search_forNumbers(Arr[offset:], Required)
        except:
            a = None
        if a != None:
            if i == 0:
                actual = a
                offset = a
            ind.append(actual)
            offset += 1
            actual += 1
        else:
            break
    if rownumber == 6:
        for i in range(len(Arr)):
            Arr[i] = Arr[i] / 10
    return ind
#----------------------------------Call This funtion to get list of indexes------------------------------
def MainofInterpolation(Arr,rownumber,Required,FilterNum):
    if(rownumber == 0 or rownumber == 1):
        if(FilterNum == 0):
            return ChangeIdxToArray(forString(Arr, rownumber, Required), Arr)
    else:
        if(FilterNum == 2):
            return ChangeIdxToArray(forNumbers(Arr, rownumber, Required),Arr)

#--------------------------------Changes index to List of attribute----------------------------------------
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

# mainList = []
# df = pd.read_csv('C:\\DSA\\Python Files\\CombineData.csv')
# for t in range(1,8):
#     List = []
#     for p in range(0,5000):
#         List.append(df.iloc[p,t])
#     mainList.append(List)
# ShellSort2.ShellSort_Asc(mainList, 0)
# l = MainofInterpolation(mainList,0,'A',0)
# print(l)