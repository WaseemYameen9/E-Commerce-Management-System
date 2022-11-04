def exchangeColumns(array, a, b, rowNumber):
    for i in range(len(array)):
        array[i][a] = array[i][b]
    return array


def exchangeObject(array, columnNo, key):
    for i in range(len(key)):
        array[i][columnNo] = key[i]


def getColumnFrom2D(arr_2, columnNo):
    arr = []
    for i in range(len(arr_2)):
        arr.append(arr_2[i][columnNo])
    return arr


def InsertionSort_asc(array_2, rowNumber):
    for i in range(1, len(array_2[rowNumber])):

        key = getColumnFrom2D(array_2, i)
        j = i - 1
        while(j >= 0 and key[rowNumber] <= array_2[rowNumber][j]):

            # array_2[j + 1] = array_2[j]
            array_2 = exchangeColumns(array_2, j+1, j, rowNumber)
            j = j - 1

        # array_2[j + 1] = key
        exchangeObject(array_2, j+1, key)

    return array_2

def InsertionSort_desc(array_2, rowNumber):
    for i in range(1, len(array_2[rowNumber])):

        key = getColumnFrom2D(array_2, i)
        j = i - 1
        while(j >= 0 and key[rowNumber] >= array_2[rowNumber][j]):

            # array_2[j + 1] = array_2[j]
            array_2 = exchangeColumns(array_2, j+1, j, rowNumber)
            j = j - 1

        # array_2[j + 1] = key
        exchangeObject(array_2, j+1, key)

    return array_2
# arr=[['ad', 'ad', 'asas', 'asd', 'ham', 'was'], ['ad', 'ad', 'asas', 'asd', 'ham', 'was']]
# print(InsertionSort_asc(arr, 0))