import math
import sys
#                               MergeSort
#______________________________________________________________________________________________________
def combineIndex(arr):
    arr = [[i, arr[i]] for i in range(len(arr))]
    return arr


def reCreateNewSortedArr(unSortedArr, sortedIndexFormat):
    sortedArr = [0]*len(unSortedArr)
    sortedArr = [[] for i in range(len(sortedArr))]
    for i in range(len(sortedIndexFormat)):
        for j in range(len(unSortedArr)):
            sortedArr[j].append(unSortedArr[j][sortedIndexFormat[i]])
    return sortedArr

#______________________________ Ascending  ____________________________________________________________
def Merge(array, p, q, r, rowNumber):

    leftArray = array[p:q+1]
    rightArray = array[q+1:r+1]
    if (isinstance(array[0][rowNumber], int) or isinstance(array[0][rowNumber], float)):
        leftArray.append([len(leftArray), sys.maxsize])
        rightArray.append([len(rightArray), sys.maxsize])
    else:
        maxlen=len(list(max([x[1] for x in leftArray])))+1
        leftArray.append([len(leftArray), ''.join([chr(255)]*maxlen)])
        rightArray.append([len(rightArray), ''.join([chr(255)]*maxlen)])

    leftArrayPointer = 0
    rightArrayPointer = 0

    i = p
    while (i <= r):
        if (leftArrayPointer<len(leftArray) and (leftArray[leftArrayPointer][rowNumber] <= rightArray[rightArrayPointer][rowNumber])):
            array[i] = leftArray[leftArrayPointer]
            leftArrayPointer += 1
        else:
            array[i] = rightArray[rightArrayPointer]
            rightArrayPointer += 1
        i += 1
    


def MergeSort(array, rowNumber, start, end):
    if (start < end):
        q = math.floor((start+end)/2)
        arr = MergeSort(array, 1, start, q)
        arr = MergeSort(array, 1, q+1, end)
        Merge(array, start, q, end, 1)


def MergeSort_asc(arr, rowNumber):
    searchRef = arr[rowNumber].copy()
    searchRef = combineIndex(searchRef)
    MergeSort(searchRef, rowNumber, 0, len(searchRef)-1)
    indexList = [x[0] for x in searchRef]
    arr = reCreateNewSortedArr(arr, indexList)
    return arr

#______________________________________ Decsending ___________________________________________________
def Merge_desc(array, p, q, r, rowNumber):

    leftArray = array[p:q+1]
    rightArray = array[q+1:r+1]

    if (isinstance(array[0][rowNumber], int) or isinstance(array[0][rowNumber], float)):
        leftArray.append([len(leftArray), -sys.maxsize ])
        rightArray.append([len(rightArray), -sys.maxsize])
    else:
        leftArray.append([len(leftArray), chr(32)])
        rightArray.append([len(rightArray), chr(32)])

    leftArrayPointer = 0
    rightArrayPointer = 0

    i = p
    while (i <= r):
        if (rightArrayPointer<len(rightArray) and leftArray[leftArrayPointer][rowNumber] >= rightArray[rightArrayPointer][rowNumber]):
            array[i] = leftArray[leftArrayPointer]
            leftArrayPointer += 1
        else:
            array[i] = rightArray[rightArrayPointer]
            rightArrayPointer += 1
        i += 1


def MergeSortDesc(array, rowNumber, start, end):
    if (start < end):
        q = math.floor((start+end)/2)
        arr = MergeSortDesc(array, 1, start, q)
        arr = MergeSortDesc(array, 1, q+1, end)
        Merge_desc(array, start, q, end, 1)


def MergeSort_desc(arr, rowNumber):
    searchRef = arr[rowNumber].copy()
    searchRef = combineIndex(searchRef)
    MergeSortDesc(searchRef, rowNumber, 0, len(searchRef)-1)
    indexList = [x[0] for x in searchRef]
    arr = reCreateNewSortedArr(arr, indexList)
    return arr
# arr=[[9,8,7,6,5,5,4,3,2,1],[0,0,0,0,5,6,6,7,8,9]]
# print(MergeSort_asc(arr,0))