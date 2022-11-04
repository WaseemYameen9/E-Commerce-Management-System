
def exchangeColumns(array, a, b, rowNumber):
    for i in range(0,7):
        c = array[i][a]
        array[i][a] = array[i][b]
        array[i][b] = c
    return array


#-----------------------Ascending-------------------------

def BrickSort_desc(array,rowNumber):
    Flag = True
    while(Flag):
        Flag = False
        for i in range(0,len(array[rowNumber])-1,2):
            if(array[rowNumber][i] < array[rowNumber][i+1]):
                array = exchangeColumns(array, i, i+1, rowNumber)
                Flag = True
                
        
        for j in range(1,len(array[rowNumber])-1,2):
            if(array[rowNumber][j] < array[rowNumber][j+1]):
                array = exchangeColumns(array, j, j+1, rowNumber)
                Flag = True
        
    return array



#-----------------------Descending------------------------------

def BrickSort_asc(array,rowNumber):
    Flag = True
    while(Flag):
        Flag = False
        for i in range(0,len(array[rowNumber])-1,2):
            if(array[rowNumber][i] > array[rowNumber][i+1]):
                array = exchangeColumns(array, i, i+1, rowNumber)
                Flag = True
                
        
        for j in range(1,len(array[rowNumber])-1,2):
            if(array[rowNumber][j] > array[rowNumber][j+1]):
                array = exchangeColumns(array, j, j+1, rowNumber)
                Flag = True
        
    return array