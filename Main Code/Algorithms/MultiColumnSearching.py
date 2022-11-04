def exchangeRowsandColumns(List):
    array = [[0 for i in range(len(List))] for j in range(7)]
    for i in range(0,len(List)):
        array[0][i] = List[i][0]
        array[1][i] = List[i][1]
        array[2][i] = List[i][2]
        array[3][i] = List[i][3]
        array[4][i] = List[i][4]
        array[5][i] = List[i][5]
        array[6][i] = List[i][6]
    return array
        

def Search(source,key,rowNumber,operator):
    if(operator == "not"):
        if(rowNumber == 0 or rowNumber == 1):
            if key in source:
                return False
        elif(key == str(source)):
            return False
        return True
    else:
        if(rowNumber == 0 or rowNumber == 1):
            if key in source:
                    return True
        elif(key == str(source)):
            return True
        


def MultiColumnSearch_1(data,rowNumber1,key1,rowNumber2,key2,operator):
    dataColumnList = []
    searchedData = []
    for i in range(0,len(data[0])):
        if(operator == "and"):
            if(Search(data[rowNumber1][i],key1,rowNumber1,operator) and Search(data[rowNumber2][i],key2,rowNumber2,operator)):
                dataColumnList.append(i)
        
        elif(operator == "or"):
            if(Search(data[rowNumber1][i],key1,rowNumber1,operator) or Search(data[rowNumber2][i],key2,rowNumber2,operator)):
                dataColumnList.append(i)
        
        elif(operator == "not"):
            if(Search(data[rowNumber1][i],key1,rowNumber1,"n") and Search(data[rowNumber2][i],key2,rowNumber2,operator)):
                dataColumnList.append(i)

    for k in range(0,len(dataColumnList)):
        lis = []
        for s in range(0,7):
            lis.append(data[s][dataColumnList[k]])
        
        searchedData.append(lis)
    Data = exchangeRowsandColumns(searchedData)
    return Data


def MultiColumnSearch_2(data,rowNumber1,key1,operator):
    dataColumnList = []
    searchedData = []
    for i in range(0,len(data[0])):
        if(operator == "and"):
            if(Search(data[rowNumber1][i],key1,rowNumber1,operator)):
                dataColumnList.append(i)
        elif(operator == "or"):
            pass
        
        
        elif(operator == "not"):
            if(Search(data[rowNumber1][i],key1,rowNumber1,operator)):
                dataColumnList.append(i)

    for k in range(0,len(dataColumnList)):
        lis = []
        for s in range(0,7):
            lis.append(data[s][dataColumnList[k]])
        
        searchedData.append(lis)
    Data = exchangeRowsandColumns(searchedData)
    return Data

