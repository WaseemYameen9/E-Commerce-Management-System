def AddinSortedArrayColumn(arr1,arr2,col,m):
    for i in range(0,7):
        arr2[i][col] = arr1[i][m]
    return arr2

def MakeratingsInteger(arr):
    for i in range(0,len(arr[0])):
        arr[6][i] = int(arr[6][i] * 10)
    return arr
    
def MakeratingsFloat(arr):
    for i in range(0,len(arr[0])):
        arr[6][i] = int(arr[6][i]) / 10
    return arr        
def sortArrayUsingCountingSort(arr,radix,rowNumber):
    indexes1 = [0 for k in range(10)]
    indexes2 = [0 for k in range(10)] 
    sortedarray = [[0 for i in range(len(arr[0]))] for j in range(7)]
    sum = 0
    
#  This loop creates an array to show how many times a number appear in main array     
    
    for i in range(0,len(arr[rowNumber])):
        num = arr[rowNumber][i]
        num2 = int(num[radix])
        indexes1[num2] = indexes1[num2] + 1

#  This loop adds the elements of indexes1 array 

    for i in range(0,10):
        indexes2[i] = sum + indexes1[i]
        sum = sum + indexes1[i]

#  This loop sorts the array according to the given radix

    for m in range(len(arr[rowNumber])-1,-1,-1):
        element = arr[rowNumber][m]
        elementsPart = int(element[radix])
        indexes2[elementsPart] = indexes2[elementsPart]-1
        sortedarray = AddinSortedArrayColumn(arr,sortedarray,indexes2[elementsPart],m)
        # sortedarray[indexes2[elementsPart]] = arr[m]
    arr = sortedarray
        
    return arr
    
    
#   Main Radix Sort Function

def RadixSort(arr,rowNumber):
    if(rowNumber == 6):
        arr = MakeratingsInteger(arr)
    maximum = max(arr[rowNumber])
    length = len(str(maximum))

# This loop will add zeros and makes all elements length same of the array  
  
    for i in range(0,len(arr[rowNumber])):
       
        num = str(arr[rowNumber][i])
        num = num.zfill(length)
        arr[rowNumber][i] = num
        

    # arr = arr[rowNumber]
    for j in range(length-1,-1,-1):
       arr = sortArrayUsingCountingSort(arr, j, rowNumber)
    if(rowNumber == 6):
        arr = MakeratingsFloat(arr)
    return arr
    

