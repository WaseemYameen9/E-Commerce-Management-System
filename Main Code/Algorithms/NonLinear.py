import numpy
import random
#from random import random_integers
import sys
import math
import xlsxwriter
import os
import csv

#______________________________________________________________________________
#               Insertions
# def exchage
def InsertionSort(arr, start, end):
    for i in range(start, end):
        value = arr[i]
        j = i-1
        while(j >= 0 and value <= arr[j]):
            arr[j+1] = arr[j]
            j = j-1
        arr[j+1] = value

#______________________________________________________________________________
#                   MergeSort
def Merge(array, p, q, r):

    leftArray = array[p:q+1]
    rightArray = array[q+1:r+1]
    
    #if(type(array)==int):    
    if(isinstance(array[0],int) or isinstance(array[0],float)):
        leftArray.append(sys.maxsize)
        rightArray.append(sys.maxsize)        
    else:
        leftArray.append("zzzzzzzzzzzzz")
        rightArray.append("zzzzzzzzzzzzz")
    
    leftArrayPointer = 0
    rightArrayPointer = 0
    
    i = p
    while(i <= r):
        if(leftArray[leftArrayPointer] <= rightArray[rightArrayPointer]):
            array[i] = leftArray[leftArrayPointer]
            leftArrayPointer += 1
        else:
            array[i] = rightArray[rightArrayPointer]
            rightArrayPointer += 1
        i += 1


def MergeSort(array, start, end):
    if(start < end):
        q = math.floor((start+end)/2)
        MergeSort(array, start, q)
        MergeSort(array, q+1, end)
        Merge(array, start, q, end)
    
#______________________________________________________________________________

# Prob 4
def HybridMergeSort(array, start, end):
    if(len(array) > 210):
        if(start < end):
            q = math.floor((start+end)/2)
            HybridMergeSort(array, start, q)
            HybridMergeSort(array, q+1, end)
            Merge(array, start, q, end)
    else:
        InsertionSort(array, start, end+1)
#______________________________________________________________________________
# Prob 5
def BubbleSort(array, start, end):
    for i in range(start, end):
        for j in range(end, i, -1):
            if(array[j] < array[j-1]):
                temp = array[j]
                array[j] = array[j-1]
                array[j-1] = temp
#______________________________________________________________________________
# Prob 6
def SelectionSort(array, start, end):
    for i in range(start, end):
        # If end is included then end +1 else end + 0
        try:
            minValue=min(array[i+1:end])  
            minIndex = array.index(minValue , i,end) 
        except:
            continue
        if(array[i] >= array[minIndex]):
            temp = array[i]
            array[i] = array[minIndex]
            array[minIndex] = temp
#______________________________________________________________________________                
# Quick Sort
def QuickSort(A,p,r):
    if(p<r):
        q=Partition(A,p,r)
        QuickSort(A,p,q-1)
        QuickSort(A,q+1,r)
def Partition(A,p,r):
    largestNumberStarting=p-1
    povit=A[r]
    for j in range(p,r):
        if(A[j] <= povit):
            largestNumberStarting+=1
            temp=A[j]
            A[j]=A[largestNumberStarting]
            A[largestNumberStarting]=temp
    A[r]=A[largestNumberStarting]
    A[largestNumberStarting]=povit
    return largestNumberStarting+1 #here the Largest Number starting and new partition needs

def ShuffleArray(arr):
    for i in range(len(arr)):
        randomNumber=random.randint(0,len(arr)-1)
        temp=arr[i]
        arr[i]=arr[randomNumber]
        arr[randomNumber]=temp
    
def saveToTheLocalFile(path, arr):
    numpy.savetxt(path, arr, delimiter=",")


def saveToTheXslsFile(path, arr):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    arr.insert(0, ['No.','Insertion','Merge','Hybrid','Bubble','Selection'])
    col = 0
    for row, data in enumerate(arr):
        worksheet.write_row (row, col, data)
    workbook.close()


# arr=[1,4,7,8,9,11,4,5,6,11,19,99]
# # arr=[1,4,7,8,9,11,22,4,5,6,11,19,99]
# # arr=[1,2,7,4,9,5,3,4,6,7,3,1,3,4,5,0,6,7,1,7,2,3,8,4]
# QuickSort(arr, 0, len(arr)-1)
# print(arr)