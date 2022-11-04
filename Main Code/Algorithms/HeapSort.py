import math

largest = 0
def Parent(i):
    return math.floor(i/2)

def Left(i):
    return 2*i

def Right(i):
    return 2*i + 1

def swapPositions(A, elem1, elem2):
     for i in range(0,7):
         (A[i])[elem1], (A[i])[elem2] = (A[i])[elem2], (A[i])[elem1]

def MaxHeapify(A, i, n,rownumber):
    l = Left(i)
    r = Right(i)
    
    if (l <= n and (A[rownumber])[l-1] > (A[rownumber])[i-1]):
        largest = l
    else:
        largest = i
    if (r <= n and (A[rownumber])[r-1] > (A[rownumber])[largest-1]):
        largest = r
    if (largest != i):
        swapPositions(A, i-1, largest-1)
        MaxHeapify(A,largest, n,rownumber)
        
def BuildMaxHeap(A,Clue,rownumber):
    n = len(A[rownumber])
    for i in range(math.floor(len(A[rownumber])/2),0,-1):
        if Clue:
            MaxHeapify(A, i, n,rownumber)
        else:
            MinHeapify(A, i, n,rownumber)
    return n
def HeapSort_Dsc(A,rownumber):
    n = BuildMaxHeap(A,False,rownumber)
    for i in range(len(A[rownumber]),1,-1):
        swapPositions(A, 0, i-1)
        n = n-1
        MinHeapify(A, 1, n,rownumber)
    return A

def HeapSort_Asc(A,rownumber):
    n = BuildMaxHeap(A,True,rownumber)
    for i in range(len(A[rownumber]),1,-1):
        swapPositions(A, 0, i-1)
        n = n-1
        MaxHeapify(A, 1, n,rownumber)        
    return A
def MinHeapify(A, i, n,rownumber):
    l = Left(i)
    r = Right(i)
    if (l <= n and (A[rownumber])[l-1] < (A[rownumber])[i-1]):
        smallest = l
    else:
        smallest = i
    if (r <= n and (A[rownumber])[r-1] < (A[rownumber])[smallest-1]):
        smallest= r
    if (smallest!= i):
        swapPositions(A, i-1, smallest-1)
        MinHeapify(A,smallest, n,rownumber)
