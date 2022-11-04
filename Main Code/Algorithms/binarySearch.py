import math
from operator import index
import sys
import math
#                                       Filters
#______________________________________________________________________________________________________
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
    if(isinstance(firstLetter, float) and isinstance(firstLetter, int)):
        firstLetter=str(firstLetter)
    if(switchingNo == 0): # start With
        return wordStartWith(firstLetter,comparisonLetter)
    if(switchingNo == 1): # End With
        return wordEndWith(firstLetter,comparisonLetter)
    if(switchingNo == 2): # Contains With
        return wordContains(firstLetter,comparisonLetter)
    if(switchingNo == 3): # Exact With
        return wordExactEquals(firstLetter,comparisonLetter)
    return False
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


def Merge(array, p, q, r, rowNumber):

    leftArray = array[p:q+1]
    rightArray = array[q+1:r+1]

    if (isinstance(array[0][rowNumber], int) or isinstance(array[0][rowNumber], float)):
        leftArray.append([len(leftArray), sys.maxsize])
        rightArray.append([len(rightArray), sys.maxsize])
    else:
        leftArray.append([len(leftArray), "zzzzzzzzzzzzz"])
        rightArray.append([len(rightArray), "zzzzzzzzzzzzz"])

    leftArrayPointer = 0
    rightArrayPointer = 0

    i = p
    while (i <= r):
        if (leftArrayPointer<len(leftArray) and leftArray[leftArrayPointer][rowNumber] <= rightArray[rightArrayPointer][rowNumber]):
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
#                       Binary Search
#______________________________________________________________________________________________________

##   Basic Logic of the algorithm
def binarySearch(startingIndex, endingIndex,filterNo, findElement, arr):
    if (startingIndex == endingIndex):
        if (compareBySwitchingCondition(arr[startingIndex],findElement,filterNo)):
            return startingIndex
        else:
            return -1
    else:
        q = math.floor((startingIndex + endingIndex)/2)
        if (compareBySwitchingCondition(arr[q],findElement,filterNo)):
            return q
        else:
            if (arr[q] > findElement):
                return binarySearch(startingIndex, q-1,filterNo, findElement, arr)
            elif (arr[q] < findElement):
                return binarySearch(q+1, endingIndex,filterNo, findElement, arr)

def checkLeftConsecutive(startingPoint, endingPoint,filterNo, findElement, arr):
    indexArr = []
    for i in range(endingPoint, startingPoint-1, -1):
        if (not compareBySwitchingCondition(arr[i],findElement,filterNo)):
            break
        indexArr.append(i)
    return indexArr


def checkRightConsecutive(startingPoint, endingPoint,filterNo, findElement, arr):
    indexArr = []
    for i in range(startingPoint, endingPoint+1):
        if (not compareBySwitchingCondition(arr[i],findElement,filterNo)):
            break
        indexArr.append(i)
    return indexArr

# implementation for the multiple Existance in the arr
def BinarySearchArr(data, rowNo,filterNo, elementFind):
    indexArr = []
    data = MergeSort_asc(data, rowNo)
    searchArr = data[rowNo].copy()
    if(isinstance(searchArr[0],float)or isinstance(searchArr[0],int)):
        searchArr=[str(x) for x in searchArr]
    firstIndex = binarySearch(0, len(searchArr)-1,filterNo, elementFind, searchArr)
    if (firstIndex != -1):
        indexArr += checkRightConsecutive(firstIndex,
                                          len(searchArr)-1,filterNo, elementFind, searchArr)
        indexArr += checkLeftConsecutive(0,
                                         firstIndex-1,filterNo, elementFind, searchArr)
    return data, list(set(indexArr))
def get1DBinarySearchData(arr,filterNo,elementFind):
    
    arr,index=BinarySearchArr([arr], 0,filterNo, elementFind)
    return [arr[0][x] for x in index]
def get2DBinarySearchData(arr, rowNo,filterNo, elementFind):
    arr, indexes = BinarySearchArr(arr, rowNo,filterNo, elementFind)
    subArr = reCreateNewSortedArr(arr, indexes)
    return subArr,indexes


def getFirstIndexByBinary(data, rowNo,filterNo, elementFind):
    data = MergeSort_asc(data, rowNo)
    searchArr = data[rowNo].copy()
    if(isinstance(searchArr[0], float) and isinstance(searchArr[0], int)):
        searchArr=[str(searchArr[i]) for i in searchArr]
    firstIndex = binarySearch(0, len(searchArr)-1,filterNo, elementFind, searchArr)
    if (firstIndex != -1):
        return firstIndex
    return None

def checkValidIndex(data,index,element):
    for row in range(len(data)):
        if(data[row][index]!=element[row]):
            return False
    return True
def deleteAtSpecificIndex(data,popIndex):
    for i in range(len(data)):
        data[i].pop(popIndex)
    return data
def deleteElementByBinarySearch(data,indexes, rowNo, elementFind):
    #  if indexes of the arr is not retirve then find 
    if(len(indexes)==0):
        data,indexes = BinarySearchArr(data, rowNo,3, elementFind[rowNo])
        
    for i in range(len(indexes)):
        if(checkValidIndex(data,indexes[i],elementFind)):
            data=deleteAtSpecificIndex(data,indexes[i])
    return data

# arr = [["was","ee","asas","ad","asd","ham","ad"],["was","ee","asas","ad","asd","ham","ad"]]
# firstIndex=binarySearch(0,len(arr[0]),0,'a',arr[0])
# arr=deleteElementByBinarySearch(arr,[],1,['ee','ee'])
# print(get2DBinarySearchData(arr,0,1,'s'))
# print(arr)
# arr = ["was","ee","asas","ad","asd","ham","ad"]
# print(get1DBinarySearchData(arr,2,'a'))