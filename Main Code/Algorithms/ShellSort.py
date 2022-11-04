import math
#-----------------------------Ascending Order------------------------------
def ShellSort_Asc(A,rownumber):
    n = math.floor(len(A[rownumber])/2)
    
    for i in range(n):
        while n>0:
            ShellInsertionSort(A,i,n,rownumber)
#    decreases GapSize until 0
            n=math.floor(n/2)
    return A
# insertion sort funtion with gapsize as an iteration length
def ShellInsertionSort(Arr,start,GapSize,rownumber):
    
    for i in range(start+GapSize,len(Arr[rownumber]),GapSize):
        current = []
        currentval = (Arr[rownumber])[i]
        ind = i
        for j in range(0,7):
            current.append((Arr[j])[i])

        while ind >= GapSize and (Arr[rownumber])[ind-GapSize] > currentval:
            (Arr[rownumber])[ind] = (Arr[rownumber])[ind-GapSize]
            exchange(Arr, ind, rownumber, GapSize)
            ind-=GapSize
            
        (Arr[rownumber])[ind] = currentval
        exchange2(Arr,ind,current,rownumber)

#----------------------------Swapping Function------------------------------
def exchange(A,ind,rownum,gap):
    for j in range(0,7):
        if(j != rownum):
            (A[j])[ind] = (A[j])[ind-gap]
def exchange2(A,ind,current,rownum):
    for j in range(0,7):
        if(j != rownum):
            (A[j])[ind] = current[j] 
# ----------------------------Descending Order-------------------------------

def ShellSort_Dsc(A,rownumber):
    n = math.floor(len(A[rownumber])/2)
    
    for i in range(n):
        while n>0:
            ShellInsertionSort2(A,i,n,rownumber)
#    decreases GapSize until 0
            n=math.floor(n/2)
    return A
# insertion sort funtion with gapsize as an iteration length
def ShellInsertionSort2(Arr,start,GapSize,rownumber):
    for i in range(start+GapSize,len(Arr[rownumber]),GapSize):
        current = []
        currentval = (Arr[rownumber])[i]
        ind = i
        for j in range(0,7):
            current.append((Arr[j])[i])

        while ind >= GapSize and (Arr[rownumber])[ind-GapSize] < currentval:
            (Arr[rownumber])[ind] = (Arr[rownumber])[ind-GapSize]
            exchange(Arr, ind, rownumber, GapSize)
            ind-=GapSize
            
            
        (Arr[rownumber])[ind] = currentval
        exchange2(Arr,ind,current,rownumber)