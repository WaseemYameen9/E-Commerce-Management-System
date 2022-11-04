def exchangeColumns(array, a, b, rowNumber):
    for i in range(0,7):
        c = array[i][a]
        array[i][a] = array[i][b]
        array[i][b] = c
    return array

#----------------For Ascending----------------------

def minimum(array , start, rowNumber):
    minimumNumber = array[rowNumber][start]
    minimumIndex = start
    for i in range(start , len(array[rowNumber])):
        if(minimumNumber > array[rowNumber][i]):
            minimumNumber = array[rowNumber][i]
            minimumIndex = i
    return minimumIndex    



def SelectionSort_asc(array , rowNumber):
    for i in range (0,len(array[rowNumber])):
        minIndex = minimum(array, i,rowNumber)
        array = exchangeColumns(array, minIndex, i, rowNumber)
    return array
        # temp = array[i]
        # array[i] = array[minIndex]
        # array[minIndex] = temp


#-----------------For Descending------------------------

def maximum(array , start, rowNumber):
    minimumNumber = array[rowNumber][start]
    minimumIndex = start
    for i in range(start , len(array[rowNumber])):
        if(minimumNumber < array[rowNumber][i]):
            minimumNumber = array[rowNumber][i]
            minimumIndex = i
    return minimumIndex    



def SelectionSort_desc(array , rowNumber):
    for i in range (0,len(array[rowNumber])):
        maxIndex = maximum(array, i,rowNumber)
        array = exchangeColumns(array, maxIndex, i, rowNumber)
    return array
        # temp = array[i]
        # array[i] = array[minIndex]
        # array[minIndex] = temp