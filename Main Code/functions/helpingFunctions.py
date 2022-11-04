from calendar import c
import pandas as pd


def getCategoriesFormTheData(df, columnName):
    dataList = df[columnName].values.tolist()
    dataList = set(dataList)
    dataList = list(dataList)
    return dataList


def getAllTheElementByCategory(categoryName, pandasData):
    # category=pandasData[categoryName]
    # x= [for x in range(len(category)) if (categoryName == category[x])]
    return pandasData


def SaveNewItemsInCSV(NewEntry, filePath):
    df = pd.read_csv(filePath)
    if (len(df) > 0):
        names = df['Name'].values.tolist()
        ActualPrices = df['Price'].values.tolist()
        price = df['Disc'].values.tolist()
        soldQuantity = df['Sold'].values.tolist()
        Reviews = df['Reviews'].values.tolist()
        Ratings = df['Ratings'].values.tolist()
        ItemType = df['Type'].values.tolist()
        #           Add new items into array
        names.append(NewEntry['Name'])
        ActualPrices.append(NewEntry['Price'])
        price.append(NewEntry['Disc'])
        soldQuantity.append(NewEntry['Sold'])
        Reviews.append(NewEntry['Reviews'])
        Ratings.append(NewEntry['Ratings'])
        ItemType.append(NewEntry['Type'])
        dataBase = {'Name': names,
                    'Type': ItemType,
                    'Price': ActualPrices,
                    'Disc': price,
                    'Sold': soldQuantity,
                    'Reviews': Reviews,
                    'Ratings': Ratings
                    }
        df = pd.DataFrame(data=dataBase)
    else:
        # ['Name','Type','Price','Disc','SoldItems','Reviews','Ratings'
        data = {'Name': [NewEntry['Name']],
                'Price': [NewEntry['Price']],
                'Disc': [NewEntry['Disc']],
                'SoldItems': [NewEntry['SoldItems']],
                'Reviews': [NewEntry['Reviews']],
                'Ratings': [NewEntry['Ratings']],
                'Type': [NewEntry['Type']]
                }
        df = pd.DataFrame(data)
    df.to_csv(filePath)


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
    if(switchingNo == 0): # start With
        return wordStartWith(firstLetter,comparisonLetter)
    if(switchingNo == 1): # End With
        return wordEndWith(firstLetter,comparisonLetter)
    if(switchingNo == 2): # Contains With
        return wordContains(firstLetter,comparisonLetter)
    if(switchingNo == 3): # Exact With
        return wordExactEquals(firstLetter,comparisonLetter)
    return False
# print(wordEndWith('hammad','ad'))
# print(wordStartWith('hammad','mam'))
# print(wordContains('Hammad','mm'))
print(compareBySwitchingCondition('hammad','ha',3))

def getDiscountedProducts(data):
    i = 0
    while(i<len(data[0])):
        if((data[2][i]) == (data[3][i])):
            data = deleteAtSpecificIndex(data, i)
        i = i + 1
            
    return data
            
def deleteAtSpecificIndex(data,popIndex):
    for i in range(len(data)):
        data[i].pop(popIndex)
    return data

#--------Return a 2d array of items within a range(Applicable on any Numerical attribute)---------
def ApplyRanging(Array,RowNumber,Starting,Ending):
    index = []
    Temp = [[Array[x][y] for y in range(len(Array[0]))] for x in range(len(Array))] #--Makes a copy without passing the reference
    
    for i in range(len(Temp[RowNumber])):
        if(float((Temp[RowNumber])[i])>= Starting and float((Temp[RowNumber])[i]) <= Ending):
            index.append(i)
            (Temp[RowNumber])[i] = -1
    return ChangeIdxToArray(index, Array)

#---------Converts Index of 2d array into Another Array
def ChangeIdxToArray(Idx,mainList):
    arr = [[0 for i in range(len(Idx))] for j in range(7)]
    for i in range(len(Idx)):
        arr[0][i] = mainList[0][Idx[i]]
        arr[1][i] = mainList[1][Idx[i]]
        arr[2][i] = mainList[2][Idx[i]]
        arr[3][i] = mainList[3][Idx[i]]
        arr[4][i] = mainList[4][Idx[i]]
        arr[5][i] = mainList[5][Idx[i]]
        arr[6][i] = mainList[6][Idx[i]]
    return arr,Idx