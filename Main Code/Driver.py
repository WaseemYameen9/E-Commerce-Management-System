from ast import operator
from configparser import Interpolation
from dataclasses import field
from logging import exception
import sys
from msilib.schema import tables
import time
from tkinter import SOLID
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import _thread
from PyQt5 import QtCore, QtGui, QtWidgets
import csv
import pandas as pd
from functions.helpingFunctions import *
from Algorithms.LinearSearch import LinearSearch_Filter
from Algorithms.InsertionSort import InsertionSort_asc, InsertionSort_desc
from Algorithms.mergeSort import MergeSort_asc, MergeSort_desc
from Algorithms.BubbleSort import BubbleSort_asc, BubbleSort_desc
from Algorithms.SelectionSort import SelectionSort_asc, SelectionSort_desc
from Algorithms.BucketSort import Bucketsort_asc, Bucketsort_desc
from Algorithms.BrickSort import BrickSort_asc, BrickSort_desc
from Algorithms.QuickSort import getsorted2DarraybyQuickSort_asc, getsorted2DarraybyQuickSort_desc
from Algorithms.PigeonHoleSort import PigeonHoleSort_asc, PigeonHoleSort_desc
from Algorithms.CountingSort import countingSort_asc, countingSort_desc
from Algorithms.HeapSort import HeapSort_Asc, HeapSort_Dsc
from Algorithms.ShellSort import ShellSort_Asc, ShellSort_Dsc
from Algorithms.RadixSort import RadixSort
from Algorithms.binarySearch import binarySearch, get2DBinarySearchData, get1DBinarySearchData, deleteElementByBinarySearch, BinarySearchArr
from Algorithms.JumpSearch import JumpSearch_Filter
from Algorithms.FibonacciSearch import MainFuncforFibnacci
from Algorithms.MultilevelSorting import InsertionSort_MultiLvlAsc, InsertionSort_MultiLvlDesc, SelectionSort_MultiLvlAsc, SelectionSort_MultiLvlDesc, BubbleSort_MultiLvlAsc, BubbleSort_MultiLvlDesc
from Algorithms.MultiColumnSearching import MultiColumnSearch_2, MultiColumnSearch_1
#  ---------Global List of Musers---------------
global acsendingElements, pandasData
acsendingElements = False
MuserList = []
dataFilePath = "Data/CombineData.csv"
CredentialFilePath = "Data/userData.csv"
pandasData = ""
sortingAlgorithms = ['Insertion Sort', 'Merge Sort', 'Selection Sort', 'Bubble Sort', 'Heap Sort', 'Quick Sort',
                     'Bucket Sort', 'Counting Sort', 'Radix Sort', 'Tim Sort', 'Shell Sort', 'Pigeonhole Sort', 'Brick Sort']
searchingAlgorithms = ['Linear Search', 'Jump Search',
                       'Interpolation Search', 'Binary Search', 'Fibonacci Search']
fields = ['Name', 'Type', 'Price', 'Disc', 'Sold', 'Reviews', 'Ratings']
comaprisonFilters = ['Start With', 'End With', 'Contains', 'Exact Equal']
MultiLevelAlgorithm = ['Insertion Sort', 'Selection Sort', 'Bubble Sort']
operaterFilter = ['and', 'or', 'not']
toggleOrderBtn = []

# ---------------------------------------------------------------------------------------------------------------
#                   Data Manager to store the Data form diffrent File


class DataManger():
    def __init__(self):
        self.DataBucket = []

    def storeData(self, data):
        self.DataBucket.append(data)

    def reteriveData(self):
        if (len(self.DataBucket) > 0):
            previousData = self.DataBucket[0]
            self.DataBucket = []
            return previousData
        return None
#  -------------Muser Class ---------------


class Muser():
    userName = ""
    userPassword = ""
    searches = []

    def __init__(self, userName, userPassword):
        self.userName = userName
        self.userPassword = userPassword

    def saveIntoTheCSV(self, filePath):
        df = pd.read_csv(filePath)  # open and read the file

        # get the user,password column
        userNames = df['UserEmail'].values.tolist()
        userPassword = df['Password'].values.tolist()

        userNames.append(self.userName)  # append the new user and password
        userPassword.append(self.userPassword)
        # create new dataFrame
        df = pd.DataFrame({
            'UserEmail': userNames,
            'Password': userPassword
        })
        df.to_csv(filePath)  # save the data frame into the file

    def IsPresent(self, filePath):
        df = pd.read_csv(filePath)  # open and read the file

        # get the user,password column
        userNames = df['UserEmail'].values.tolist()
        userPasswords = df['Password'].values.tolist()
        print(self.userName, self.userPassword)
        for i in range(len(userNames)):
            if self.userName == userNames[i] and self.userPassword == userPasswords[i]:
                return True
        return False
# ---------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------
#  -------------Main Dashboard Class ---------------

class Dashboard(QMainWindow):
    offset = 135
    Limitation = 0
    multiColFields = []

    def __init__(self, user, data):
        self.algorithmStartingTime = 0
        self.algorithmEndingTime = 0
        self.user = user
        self.pandasData = data
        self.ViewCategoriesTableData = data
        self.dataBucket = DataManger()
        super(Dashboard, self).__init__()
        loadUi("UI/MainDashboard.ui", self)
        self.showDashboard()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QtGui.QIcon('resources\shopping-cart (1).png'))
        self.setWindowTitle('E-Commerce Management System')
        self.setFixedWidth(self.width())
        self.setFixedHeight(self.height())
        # fillComboBox(self.fieldCombobox, fields)
        fillComboBox(self.sortingComboBox, sortingAlgorithms)
        self.checkAlgorithmLimitations()
        fillComboBox(self.categoryCombobox,
                     getCategoriesFormTheData(pandasData, 'Type'))
        self.accountName.setText(self.user.userName)
        self.mainSearchComboBox.currentTextChanged.connect(
            self.SearchMainComboBoxText)
        # ---------Main Dashboard all click events---------
        self.viewItemsBtn.clicked.connect(self.showViewItems)
        self.categoryBtn.clicked.connect(self.showCategories)
        self.dashBoardBtn.clicked.connect(self.showDashboard)
        self.scrappingBtn.clicked.connect(self.showScrapping)
        self.discountBtn.clicked.connect(self.showDiscount)
        self.signOutBtn.clicked.connect(self.closeWindowSaveIntoCsv)
        self.addItem.mouseReleaseEvent = self.addNewItem
        self.delItem.mouseReleaseEvent = self.deleteExitedItem
        self.editItem.mouseReleaseEvent = self.editExitedItem
        # --------- Scraping Page Click ----------------
        self.scrapBtn.clicked.connect(self.scrap)
        # ---------- View Items Page Click Event ------------------
        self.searchBtn.clicked.connect(self.showfilterDialogWindow)
        self.rangeBtn.clicked.connect(self.showRangeDialogWindow)
        self.sortBtn.clicked.connect(self.showSortedArrInTable)
        self.viewTable.cellClicked.connect(self.isCellClicked)
        self.multiLvlBtn.clicked.connect(self.MultiLVlDialogWindow)
        # ---------- Categories Page Click Event ------------------
        self.categorySearchBtn.clicked.connect(
            self.DispalySepecificCategoryItem)
        # ---------- Combo Box Click Event ------------------------
        self.sortingComboBox.currentIndexChanged.connect(
            self.checkAlgorithmLimitations)
        # ----------  Page Click Event ------------------
        # ----------Search Page events --------------
        self.MultiSearchBtn.clicked.connect(self.showMultiColSearchUI)

    # ---------------- Main search ComboBox Funtion ---------------
    def SearchMainComboBoxText(self):
        arr = []
        try:
            searchTxt = removeStartingSpaceInString(
                self.mainSearchComboBox.currentText())
            self.pandasData = pd.read_csv(dataFilePath)
            arr = convertPandasInto2Darray(self.pandasData, fields)
            arr = get1DBinarySearchData(arr[0], 0, searchTxt)
        except:
            arr = []
        if (len(arr) > 0):
            fillComboBox(self.mainSearchComboBox, arr[0:10])
        else:
            fillComboBox(self.mainSearchComboBox, ['Select Another KeyWords'])
        # mainSearchComboBox
    # ----------All Functions for Main Dashboard------------------

    def showViewItems(self):
        self.setWindowTitle('E-Commerce Management System - View Items')
        self.stackedWidget.setCurrentWidget(self.ViewItems_2)
        # acsendingElements = False
        fillTable(self.viewTable, self.pandasData, fields)

    def showSortedArrInTable(self):
        algorithm = self.sortingComboBox.currentText()
        self.setWindowTitle(
            'E-Commerce Management System - View Items - Loading')
        fieldSelect = self.fieldCombobox.currentText()
        algorithmIndex = sortingAlgorithms.index(algorithm)
        fieldIndex = fields.index(fieldSelect)
        # sortingAlgorithms = ['Insertion Sort', 'Merge Sort', 'Selection Sort', 'Bubble Sort', 'Heap Sort', 'Quick Sort',
        #              'Bucket Sort', 'Counting Sort', 'Radix Sort', 'Tim Sort', 'Shell Sort', 'Pigeonhole Sort', 'Brick Sort']
        arr = convertPandasInto2Darray(self.pandasData, fields)
        sortedArr = []
        self.algorithmStartingTime = time.time()
        if (algorithmIndex == 0):
            sortedArr = InsertionSort_asc(arr, fieldIndex)
        elif (algorithmIndex == 1):
            sortedArr = MergeSort_asc(arr, fieldIndex)
        elif (algorithmIndex == 2):
            sortedArr = SelectionSort_asc(arr, fieldIndex)
        elif (algorithmIndex == 3):
            sortedArr = BubbleSort_asc(arr, fieldIndex)
        elif (algorithmIndex == 4):
            sortedArr = HeapSort_Asc(arr, fieldIndex)
        elif (algorithmIndex == 5):
            sortedArr = getsorted2DarraybyQuickSort_asc(arr, fieldIndex)
        elif (algorithmIndex == 6):
            sortedArr = Bucketsort_asc(arr, fieldIndex)
        elif (algorithmIndex == 7):
            sortedArr = countingSort_asc(arr, fieldIndex)
        elif (algorithmIndex == 8):
            sortedArr = RadixSort(arr, fieldIndex)
        # elif(algorithmIndex ==9):
        #     sortedArr=TimSort(arr,fieldIndex)
        elif (algorithmIndex == 10):
            sortedArr = ShellSort_Asc(arr, fieldIndex)
        elif (algorithmIndex == 11):
            sortedArr = PigeonHoleSort_asc(arr, fieldIndex)
        elif (algorithmIndex == 12):
            sortedArr = BrickSort_asc(arr, fieldIndex)
        self.consumeTimeTxt.setText(
            str(time.time()-self.algorithmStartingTime))
        arr = convert2DarrayInPandas(sortedArr)
        fillTable(self.viewTable, arr, fields)
        self.setWindowTitle('E-Commerce Management System - View Items')

    def showCategories(self):
        self.setWindowTitle('E-Commerce Management System - Categories')
        self.stackedWidget.setCurrentWidget(self.Category)

    def showScrapping(self):
        self.setWindowTitle('E-Commerce Management System - Scrapping')
        self.stackedWidget.setCurrentWidget(self.Scrapping_2)

    def showDiscount(self):
        self.setWindowTitle('E-Commerce Management System - Discounts')
        self.stackedWidget.setCurrentWidget(self.Discount)

    def showDashboard(self):
        self.setWindowTitle('E-Commerce Management System - DashBoard')
        self.stackedWidget.setCurrentWidget(self.dashBoard)

    def closeWindowSaveIntoCsv(self):
        self.close()

    def addNewItem(self, event):
        newItemDialogWindow = AddItemUI()
        newItemDialogWindow.exec()
        print('Add Btn clicked')
        self.pandasData = pd.read_csv(dataFilePath)

    def deleteExitedItem(self, event):
        delItemDialog = DelItemUI()
        delItemDialog.exec()
        self.pandasData = pd.read_csv(dataFilePath)

    def editExitedItem(self, event):
        print('Edit Btn clicked')
    # -------Write Functions of Sub Pages Here-------------

    def scrap(self):

        msg = QMessageBox()
        msg.setWindowTitle("Scrap")
        msg.setText("Scrap is Clicked")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def showfilterDialogWindow(self):
        filterWindow = filterDialogUI(self.dataBucket)
        # fillTable(self.vi)
        filterWindow.exec()
        pandasSearchData = self.dataBucket.reteriveData()
        try:
            self.ViewCategoriesTableData = pandasSearchData
            fillTable(self.viewTable, pandasSearchData, fields)
        except:
            showErrorMessageBox('No Match Found')

    def showRangeDialogWindow(self):
        rangeWindow = rangeDialogUI(
            self.dataBucket, self.ViewCategoriesTableData)
        rangeWindow.show()
        rangeWindow.exec()
        data = self.dataBucket.reteriveData()
        try:
            self.ViewCategoriesTableData
            fillTable(self.viewTable, self.pandasSearchData, fields)
        except:
            showErrorMessageBox('Not Search Found')
    # -------           View Items          -------------

    def DispalySepecificCategoryItem(self):
        # ---------------- insert the headers -----------------------------------------------
        specificCategory = self.categoryCombobox.currentText()
        algorithmData = [self.pandasData[i].values.tolist() for i in fields]
        index = 1
        # outputSort=LinearSearch(algorithmData,index,specificCategory)
        outputSort, garbage = get2DBinarySearchData(
            algorithmData, index, 2, specificCategory)
        # outputSort=JumpSearch_Filter(algorithmData,index,specificCategory)
        outputPandasSort = convert2DarrayInPandas(outputSort)
        fillTable(self.categoriesTable, outputPandasSort, fields)

    def checkAlgorithmLimitations(self):
        print(self.sortingComboBox.currentText())
        index = sortingAlgorithms.index(self.sortingComboBox.currentText())
        if index in {6, 7,8, 11}:
            nonStringFields = fields[2:]
            fillComboBox(self.fieldCombobox, nonStringFields)
        else:
            fillComboBox(self.fieldCombobox, fields)

    def isCellClicked(self, row, column):
        print(row, ' ', column)
        if (row == 0 and (column >= 0 and column < 8)):
            self.setWindowTitle(
                'E-Commerce Management System - View Items - Loading')
            algorithm = self.sortingComboBox.currentText()
            fieldSelect = self.fieldCombobox.currentText()
            algorithmIndex = sortingAlgorithms.index(algorithm)
            fieldIndex = column
            # sortingAlgorithms = ['Insertion Sort', 'Merge Sort', 'Selection Sort', 'Bubble Sort', 'Heap Sort', 'Quick Sort',
            #              'Bucket Sort', 'Counting Sort', 'Radix Sort', 'Tim Sort', 'Shell Sort', 'Pigeonhole Sort', 'Brick Sort']
            arr = convertPandasInto2Darray(self.pandasData, fields)
            sortedArr = []
            self.algorithmStartingTime = time.time()
            if (algorithmIndex == 0):
                sortedArr = InsertionSort_desc(arr, fieldIndex)
            if (algorithmIndex == 1):
                sortedArr = MergeSort_desc(arr, fieldIndex)
            if (algorithmIndex == 2):
                sortedArr = SelectionSort_desc(arr, fieldIndex)
            if (algorithmIndex == 3):
                sortedArr = BubbleSort_desc(arr, fieldIndex)
            if (algorithmIndex == 4):
                sortedArr = HeapSort_Dsc(arr, fieldIndex)
            if (algorithmIndex == 5):
                sortedArr = getsorted2DarraybyQuickSort_desc(arr, fieldIndex)
            if (algorithmIndex == 6):
                sortedArr = Bucketsort_desc(arr, fieldIndex)
            if (algorithmIndex == 7):
                sortedArr = countingSort_desc(arr, fieldIndex)
            # if(algorithmIndex ==8):
            #     sortedArr=RadixSort(arr,fieldIndex)
            # if(algorithmIndex ==9):
            #     sortedArr=TimSort(arr,fieldIndex)
            if (algorithmIndex == 10):
                sortedArr = ShellSort_Dsc(arr, fieldIndex)
            if (algorithmIndex == 11):
                sortedArr = PigeonHoleSort_desc(arr, fieldIndex)
            if (algorithmIndex == 12):
                sortedArr = BrickSort_desc(arr, fieldIndex)
            self.consumeTimeTxt.setText(
                str(time.time()-self.algorithmStartingTime))
            arr = convert2DarrayInPandas(sortedArr)
            fillTable(self.viewTable, arr, fields)
            self.setWindowTitle('E-Commerce Management System - View Items')

    def MultiLVlDialogWindow(self):
        multiLvl = MultiLevelSortingUI(self.dataBucket)
        multiLvl.show()
        multiLvl.exec()
        MultiLevelPageData = self.dataBucket.reteriveData()
        # data={'Algorithm':self.SortingAlgorithmComboBox.currentText(),
        # 'orderList':self.orderList,
        # 'ascending':ascending}

        if (MultiLevelPageData != None):
            orderList = MultiLevelPageData['orderList']
            acsendingBool = MultiLevelPageData['ascending']
            algorithmIndex = MultiLevelAlgorithm.index(
                MultiLevelPageData['Algorithm'])
            self.pandasData = pd.read_csv(dataFilePath)
            pandas2DArr = convertPandasInto2Darray(self.pandasData, fields)
            # MultiLevelAlgorithm = ['Insertion Sort', 'Selection Sort', 'Bubble Sort']

            self.setWindowTitle(
                'E-Commerce Management System - View Items - Loading')

            if (algorithmIndex == 0):
                if (acsendingBool):
                    pandas2DArr = InsertionSort_MultiLvlAsc(
                        pandas2DArr, orderList[0], orderList[1:])
                else:
                    InsertionSort_MultiLvlDesc(
                        pandas2DArr, orderList[0], orderList[1:])
            elif (algorithmIndex == 1):
                if (acsendingBool):
                    pandas2DArr = SelectionSort_MultiLvlAsc(
                        pandas2DArr, orderList[0], orderList[1:])
                else:
                    pandas2DArr = SelectionSort_MultiLvlDesc(
                        pandas2DArr, orderList[0], orderList[1:])
            elif (algorithmIndex == 2):
                if (acsendingBool):
                    pandas2DArr = BubbleSort_MultiLvlAsc(
                        pandas2DArr, orderList[0], orderList[1:])
                else:
                    pandas2DArr = BubbleSort_MultiLvlDesc(
                        pandas2DArr, orderList[0], orderList[1:])
            self.consumeTimeTxt.setText(
                str(time.time()-self.algorithmStartingTime))
            sortedPandas = convert2DarrayInPandas(pandas2DArr)
            fillTable(self.viewTable, sortedPandas, fields)
            self.setWindowTitle('E-Commerce Management System - View Items')

    # def generateCombobox(self):
    #     if(self.Limitation < 7):
    #         FilterCombobox=None
    #         fieldNameComboBox=None
    #         Lineedit=None
    #         if(self.Limitation%2 == 0):
    #             if(self.Limitation != 0):
    #                 FilterCombobox = QComboBox(self)
    #                 fillComboBox(FilterCombobox,operaterFilter)
    #                 FilterCombobox.setObjectName('FilterCombobox'+str(self.Limitation))
    #                 FilterCombobox.move(185,self.offset)
    #                 FilterCombobox.adjustSize()
    #                 FilterCombobox.show()

    #             fieldNameComboBox = QComboBox(self)
    #             fillComboBox(fieldNameComboBox,fields)
    #             fieldNameComboBox.move(250,self.offset)
    #             fieldNameComboBox.adjustSize()
    #             fieldNameComboBox.setObjectName('fileNameComboBox'+str(self.Limitation))
    #             fieldNameComboBox.show()

    #             Lineedit = QLineEdit(self)
    #             Lineedit.setPlaceholderText('Text')
    #             Lineedit.move(350,self.offset)
    #             Lineedit.setObjectName('Hello')
    #             Lineedit.resize(180, 20)
    #             Lineedit.setObjectName('Lineedit'+str(self.Limitation))
    #             Lineedit.show()
    #             self.Limitation += 1
    #         else:
    #             FilterCombobox = QComboBox(self)
    #             fillComboBox(FilterCombobox,operaterFilter)
    #             FilterCombobox.move(530,self.offset)
    #             FilterCombobox.setObjectName('Hello')
    #             FilterCombobox.adjustSize()
    #             FilterCombobox.setObjectName('FilterCombobox'+str(self.Limitation))
    #             FilterCombobox.show()
    #             fieldNameComboBox = QComboBox(self)
    #             fillComboBox(fieldNameComboBox,fields)
    #             fieldNameComboBox.move(595,self.offset)
    #             fieldNameComboBox.adjustSize()
    #             fieldNameComboBox.setObjectName('Hello')
    #             fieldNameComboBox.setObjectName('fileNameComboBox'+str(self.Limitation))
    #             fieldNameComboBox.show()

    #             Lineedit = QLineEdit(self)
    #             Lineedit.setPlaceholderText('Text')
    #             Lineedit.move(700,self.offset)
    #             Lineedit.resize(180, 20)
    #             Lineedit.setObjectName('Hello')
    #             Lineedit.setObjectName('Lineedit'+str(self.Limitation))
    #             Lineedit.show()
    #             self.Limitation += 1
    #             self.offset += 30
    #         self.multiColFields.append([FilterCombobox,fieldNameComboBox,Lineedit])

    def showMultiColSearchUI(self):
        multiColWindow = MultiColumnUi(self.dataBucket)
        multiColWindow.show()
        multiColWindow.exec()
        MultiSearchedData = self.dataBucket.reteriveData()
        try:
            fillTable(self.multilevelTabel, MultiSearchedData, fields)
        except:
            showPopUpMessageBox('Error !','No Match Found')
            fillTable(self.multilevelTabel, self.pandasData, fields)

# ------------ FilterUI class------------


class MultiColumnUi(QDialog):
    def __init__(self, dataBucket):
        super(MultiColumnUi, self).__init__()
        loadUi("UI\multiColSearching.ui", self)
        # UI/multiColSearching.ui
        self.setWindowTitle('Mutli Column Search')
        self.pandasData = pd.read_csv(dataFilePath)
        self.dataBucket = dataBucket
        self.operators = []
        self.selectedfields = []
        self.searchText = []
        fillComboBox(self.operatorComboBox, operaterFilter)
        fillComboBox(self.fieldComboBox, fields)
        self.addBtn.clicked.connect(self.AddNewSearchType)
        self.okBtn.clicked.connect(self.SendBackSearchData)

    def alreadyPresent(self,fieldselected, searchText, operatorSign):
        for i in range(len(self.operators)):
            if(fieldselected == self.selectedfields[i] and searchText == self.searchText[i] and operatorSign==self.operators[i]):
                return True
        return False

    def AddNewSearchType(self):
        fieldselected = fields.index(self.fieldComboBox.currentText())
        searchText = removeStartingSpaceInString(self.findTxt.text())
        if (searchText != ''):
            # if (alreadyPresent(self,fieldselected, searchText, self.operatorComboBox.currentText())==False):
            if (fieldselected > 1):  # NonStringFields
                try:
                    if (float(searchText) > -1):
                        if (len(self.selectedfields) > 0):
                            self.operators.append(
                                self.operatorComboBox.currentText())
                            self.selectedfields.append(
                                self.fieldComboBox.currentText())
                            self.searchText.append(searchText)
                        else:
                            self.operators.append("")
                            self.selectedfields.append(
                                self.fieldComboBox.currentText())
                            self.searchText.append(searchText)
                        self.updateMultiColumnTable()
                except Exception as e:
                    showErrorMessageBox(str(e))
            else:  # StringFields
                if(len(self.selectedfields) > 0):
                    self.operators.append(
                        self.operatorComboBox.currentText())
                    self.selectedfields.append(
                        self.fieldComboBox.currentText())
                    self.searchText.append(searchText)
                else:
                    self.operators.append("")
                    self.selectedfields.append(
                        self.fieldComboBox.currentText())
                    self.searchText.append(searchText)
                self.updateMultiColumnTable()
        self.findTxt.setText('')
    
    def SendBackSearchData(self):
        if(len(self.selectedfields) > 0):
            dataArr = convertPandasInto2Darray(self.pandasData, fields)
            if(len(self.selectedfields) == 1):            
                rowNo1 = fields.index(self.selectedfields[0])
                dataArr = MultiColumnSearch_2(dataArr, rowNo1,self.searchText[0],'and')
                print(dataArr)
            elif(len(self.selectedfields) > 1):
                rowNo1 = fields.index(self.selectedfields[0])
                rowNo2 = fields.index(self.selectedfields[1])
                # MultiColumnSearch_2(data,rowNo,self.searchText[i],'and')
                dataArr = MultiColumnSearch_1(dataArr, rowNo1,self.searchText[0],rowNo2,self.searchText[1],self.operators[1])
                # dataArr=MultiColumnSearch_1(dataArr,0,'5',2,'720','and')
                for i in range(2, len(self.searchText)):
                    rowNo = fields.index(self.selectedfields[i])
                    rowNo = fields.index(self.selectedfields[i])
                    dataArr = MultiColumnSearch_2(dataArr, rowNo,self.searchText[i],self.operators[i])
            if(len(dataArr[0])==0):
                showErrorMessageBox('Match Not Found')
                dataArr=self.pandasData
            else:
                dataArr = convert2DarrayInPandas(dataArr)
            self.dataBucket.storeData(dataArr)
            self.close()

    def updateMultiColumnTable(self):
        arr2D = {'operator': self.operators,'Fields':self.selectedfields,'Search':self.searchText}
        arrPandas = pd.DataFrame(arr2D)
        fillMultiColTable(self.multilevelTable, arrPandas, ['operator','Fields','Search'])


class filterDialogUI(QDialog):
    def __init__(self, dataBucket):
        self.dataBucket = dataBucket
        self.pandasData = pd.read_csv(dataFilePath)
        super(filterDialogUI, self).__init__()
        loadUi("UI/filterContsinsDialog.ui", self)
        self.setWindowTitle('Filter')
        fillComboBox(self.filterComboBox, comaprisonFilters)
        fillComboBox(self.fieldNameComboBox, fields)
        fillComboBox(self.algorithmComboBox, searchingAlgorithms)
        self.algorithmComboBox.currentIndexChanged.connect(
            self.checkSearchLimitation)
        self.okBtn.clicked.connect(self.ReceiveFilter)

    def ReceiveFilter(self):
        Fieldindex = fields.index(self.fieldNameComboBox.currentText())
        findTxt = removeStartingSpaceInString(self.containsTxt.text())
        filterNo = comaprisonFilters.index(self.filterComboBox.currentText())
        algorithmIndex = searchingAlgorithms.index(
            self.algorithmComboBox.currentText())
        arr = convertPandasInto2Darray(self.pandasData, fields)
        if (algorithmIndex == 0):
            arr, index = LinearSearch_Filter(
                arr, Fieldindex, findTxt, filterNo)
        elif (algorithmIndex == 1):
            arr, index = JumpSearch_Filter(arr, Fieldindex, findTxt, filterNo)
        elif (algorithmIndex == 2):
            a = 0
            # arr,index=Interpolation(arr,Fieldindex,findTxt,filterNo)
        elif (algorithmIndex == 3):
            arr, index = get2DBinarySearchData(
                arr, Fieldindex, filterNo, findTxt)
        elif (algorithmIndex == 4):
            arr, index = MainFuncforFibnacci(
                arr, Fieldindex, findTxt, filterNo)
        # add arr pandas data tot the bucket
        self.dataBucket.storeData(convert2DarrayInPandas(arr))
        self.close()

    def checkSearchLimitation(self):
        if(self.algorithmComboBox.currentText() == 'Interpolation Search'):
            fillComboBox(self.fieldNameComboBox, fields[2:])

# ------------ RangeUI class------------


class rangeDialogUI(QDialog):
    def __init__(self, dataBucket, pandasData):
        self.dataBucket = dataBucket
        self.pandasData = pandasData
        super(rangeDialogUI, self).__init__()
        loadUi("UI/rangeDialog.ui", self)
        self.setWindowTitle('Range')
        fillComboBox(self.fieldComboBox, fields[2:])
        self.okBtn.clicked.connect(self.ReceiveRangeDetails)

    def ReceiveRangeDetails(self):
        endTxt = float(removeStartingSpaceInString(self.endTxt.text()))
        starttxt = float(removeStartingSpaceInString(self.startTxt.text()))
        fieldNo = fields.index(self.fieldComboBox.currentText())
        arr = convertPandasInto2Darray(self.pandasData, fields)
        requiredData = ApplyRanging(arr, fieldNo, fieldNo,endTxt)
        self.dataBucket.storeData(convert2DarrayInPandas(requiredData))
        self.close()

# ------------SignInUI class-------------


class signInUI(QDialog):
    def __init__(self):
        super(signInUI, self).__init__()
        loadUi("UI/SignInDialog.ui", self)
        self.setWindowTitle('Sign In')
        self.loginBtn.clicked.connect(self.IsUser)
        self.signupBtn.clicked.connect(self.showSignUpWindow)

    def IsUser(self):
        newUserName = self.emailTxt.text()
        newUserPassword = self.passTxt.text()
        logInUser = Muser(newUserName, newUserPassword)
        if (logInUser.IsPresent(CredentialFilePath)):
            self.close()
            pandasData = pd.read_csv(dataFilePath)
            self.window1 = Dashboard(logInUser, pandasData)
            self.window1.show()
        else:
            msg = QMessageBox()
            self.passTxt.setText('')
            msg.setWindowTitle("New to app")
            msg.setText("You are not registered! kindly SignUp")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def showSignUpWindow(self):
        self.close()
        self.window1 = signUpUI()
        self.window1.show()

#  ------------SignUpUI class----------


class signUpUI(QDialog):
    def __init__(self):
        super(signUpUI, self).__init__()
        loadUi("UI/SignUpDialog.ui", self)
        self.setWindowTitle('Sign Up')
        self.registerBtn.clicked.connect(self.AddUser)

    def AddUser(self):
        userName = self.EmailTxt.text()
        userPassword = self.passwordTxt.text()
        # check the Both Password & confirm password is Same
        if (userPassword == self.passwordTxt_2.text()):
            newUser = Muser(userName, userPassword)
            if (newUser.IsPresent(CredentialFilePath)):
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Account is Already Exist")
                msg.setIcon(QMessageBox.Critical)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
            else:
                newUser.saveIntoTheCSV(CredentialFilePath)
            self.close()
            self.window1 = signInUI()
            self.window1.show()
            self.window1.setWindowTitle('E-commerce Sign In')

        else:
            showErrorMessageBox("Both Passwords doesn't match")
#  ------------Add Dialog class----------


class AddItemUI(QDialog):
    def __init__(self):
        super(AddItemUI, self).__init__()
        loadUi("UI/adddNewUser.ui", self)
        self.setWindowTitle('Add New Item')
        self.okBtn.clicked.connect(self.AddItem)
        self.pandasData = pd.read_csv(dataFilePath)

    def AddItem(self):
        itemName = removeStartingSpaceInString(self.nameTxt.text())
        itemType = removeStartingSpaceInString(self.typeTxt.text())
        pandasData = pd.read_csv(dataFilePath)
        twoDarr = convertPandasInto2Darray(pandasData, fields)
        twoArr, findSimilarItem = BinarySearchArr(twoDarr, 0, 3, itemName)
        # twoArr,findSimilarItem=JumpSearch_Filter(twoDarr,0,itemName,)
        #               Check Validations
        try:
            itemDisc = float(removeStartingSpaceInString(self.discTxt.text()))
            itemPrice = float(
                removeStartingSpaceInString(self.priceTxt.text()))
            itemSold = int(removeStartingSpaceInString(self.soldTxt.text()))
            itemReview = int(
                removeStartingSpaceInString(self.reviewTxt.text()))
            itemRating = float(
                removeStartingSpaceInString(self.ratingTxt.text()))
            if (len(findSimilarItem) == 0):
                if (itemSold >= 0 and itemPrice >= 0 and itemPrice >= itemDisc and itemDisc >= 0 and applyLimitRangeInt(itemRating, -1, 6)):
                    dataSet = {'Name': itemName,
                               'Type': itemType,
                               'Price': itemPrice,
                               'Disc': itemDisc,
                               'Sold': itemSold,
                               'Reviews': itemReview,
                               'Ratings': itemRating
                               }
                    if (not isAlreadyPresentInArray(findSimilarItem, dataSet)):
                        SaveNewItemsInCSV(dataSet, dataFilePath)
                        pandasData = pd.read_csv(dataFilePath)
                        self.close()
                else:
                    showErrorMessageBox(
                        'You should be enter realistic information')
            else:
                showErrorMessageBox('Already present')
        except Exception as e:
            showErrorMessageBox(str(e))

#       DeleteUI class


class DelItemUI(QDialog):
    def __init__(self):
        super(DelItemUI, self).__init__()
        loadUi("UI/deleteItem.ui", self)
        self.setWindowTitle('Delete Item')
        fillComboBox(self.fieldComboBox, fields)
        fillComboBox(self.filterComboBox, comaprisonFilters)
        self.delBtn.clicked.connect(self.DelItem)
        self.DisplayBtn.clicked.connect(self.DisplayItem)
        self.pandasData = pd.read_csv(dataFilePath)
        self.indexSearch = []

    def DisplayItem(self):
        self.pandasData = pd.read_csv(dataFilePath)
        arr = convertPandasInto2Darray(self.pandasData, fields)
        searchTxt = removeStartingSpaceInString(self.searchTxt.text())

        selectField = self.fieldComboBox.currentText()
        srNoTxt = self.srNoTxt.text()

        if (searchTxt != ''):
            rowNo = fields.index(selectField)
            switchingComparisonNo = comaprisonFilters.index(
                self.filterComboBox.currentText())
            # panda=convert2DarrayInPandas(arr)
            try:
                if (switchingComparisonNo == 2):
                    arr, self.indexSearch = LinearSearch_Filter(
                        arr, rowNo, searchTxt, switchingComparisonNo)

                else:
                    # arr, self.indexSearch = get2DBinarySearchData(arr, rowNo , switchingComparisonNo , searchTxt)
                    arr, self.indexSearch = JumpSearch_Filter(
                        arr, rowNo, searchTxt, switchingComparisonNo)
                    # arr,self.indexSearch= MainFuncforFibnacci(arr,rowNo,searchTxt,switchingComparisonNo)
                panda = convert2DarrayInPandas(arr)
            except:
                panda = self.pandasData
                showErrorMessageBox('Not Found')
            fillTable(self.searchDisplayTable, panda, fields)
        else:
            fillTable(self.searchDisplayTable, self.pandasData, fields)

    def DelItem(self):
        try:
            self.pandasData = pd.read_csv(dataFilePath)
            srNo = int(removeStartingSpaceInString(self.srNoTxt.text()))
            index = self.indexSearch[srNo-2]
            selectField = self.fieldComboBox.currentText()
            arr = convertPandasInto2Darray(self.pandasData, fields)  # convert
            fieldIndex = fields.index(selectField)

            arr = MergeSort_asc(arr, fieldIndex)
            itemName = arr[0][index]
            itemType = arr[1][index]
            itemPrice = arr[2][index]
            itemDisc = arr[3][index]
            itemSold = arr[4][index]
            itemRating = arr[5][index]
            itemReviews = arr[6][index]
            itemDetails = [itemName, itemType, itemPrice,
                           itemDisc, itemSold, itemRating, itemReviews]
            print(itemDetails)
            arr = deleteElementByBinarySearch(arr, [index], 0, itemDetails)
            self.pandasData = convert2DarrayInPandas(arr)
            self.pandasData.to_csv(dataFilePath)
            showPopUpMessageBox('Done', 'Item Scussefully Deleted')
            self.srNoTxt.setText('')
            self.DisplayItem()
        except Exception as e:
            showErrorMessageBox(str(e))
# -----------------------------------------------------------------------------------------------------------------
#                                       Helping Functions


def isAlreadyPresentInArray(twoDarr, dataSet):
    if (len(twoDarr) > 0):
        for i in range(len(twoDarr[0])):
            if (twoDarr[0][i] == dataSet[fields[i]] and twoDarr[1][i] == dataSet[fields[i]] and twoDarr[2][i] == dataSet[fields[i]] and twoDarr[3][i] == dataSet[fields[i]] and twoDarr[4][i] == dataSet[fields[i]] and twoDarr[5][i] == dataSet[fields[i]] and twoDarr[6][i] == dataSet[fields[i]]):
                return True
    return False


def IsNonStringFieldConvertIntoInt(arr):
    try:
        for i in arr:
            grabageVariable = int(i)
        return True
    except:
        return False


def showErrorMessageBox(message):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(message)
    msg.setIcon(QMessageBox.Critical)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()


def showPopUpMessageBox(title, message):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()


def checkNonEmptyLimit(arr):
    for i in arr:
        if (i == ' '):
            return True
    return False


def removeStartingSpaceInString(text):
    text = list(text)
    lengthoftext = len(text)
    i = 0
    while (i < lengthoftext):
        if (text[i] == ' '):
            text.pop(i)
            lengthoftext = len(text)
        else:
            break
        i += 1
    return ''.join(text)


def applyLimitRangeInt(no, starting, ending):
    if (no > starting and no < ending):
        return True
    else:
        return False


def convert2DarrayInPandas(arr):
    data = {
        'index': [0]*len(arr[1]),
        'Name': arr[0],
        'Type': arr[1],
        'Price': arr[2],
        'Disc': arr[3],
        'Sold': arr[4],
        'Reviews': arr[5],
        'Ratings': arr[6]
    }
    data = pd.DataFrame(data)
    return data


def convertPandasInto2Darray(df, fieldNames):
    arr = []
    for i in fieldNames:
        arr.append(df[i].values.tolist())
    return arr


def fillComboBox(comboBox, datalist):
    comboBox.clear()
    comboBox.addItems(datalist)
    comboBox.setCurrentIndex(0)


def fillTable(categoryTable, data, header):
    rows = len(data)
    categoryTable.setRowCount(rows+1)
    categoryTable.setColumnCount(7)
    for i in range(len(header)):
        headerName = QTableWidgetItem(header[i])
        categoryTable.setItem(0, i, headerName)
        categoryTable.item(0, i).setBackground(QtGui.QColor(0, 85, 255))
        categoryTable.item(0, i).setFont(QtGui.QFont('MS Shell Dlg 2', 14))
    # categoryTable.setHorizontalHeaderLabels(header)
    for m in range(0, rows):
        productName = QTableWidgetItem(data.iloc[m, 1])
        productType = QTableWidgetItem(data.iloc[m, 2])
        actualPrice = QTableWidgetItem(str(data.iloc[m, 3]))
        discountedPrice = QTableWidgetItem(str(data.iloc[m, 4]))
        soldQty = QTableWidgetItem(str(data.iloc[m, 5]))
        reviews = QTableWidgetItem(str(data.iloc[m, 6]))
        ratings = QTableWidgetItem(str(data.iloc[m, 7]))
        categoryTable.setItem(m+1, 0, productName)
        categoryTable.setItem(m+1, 1, productType)
        categoryTable.setItem(m+1, 2, actualPrice)
        categoryTable.setItem(m+1, 3, discountedPrice)
        categoryTable.setItem(m+1, 4, soldQty)
        categoryTable.setItem(m+1, 5, reviews)
        categoryTable.setItem(m+1, 6, ratings)
    categoryTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    categoryTable.resizeColumnsToContents()
    categoryTable.resizeRowsToContents()

def fillMultiColTable(categoryTable, data, header):
    rows = len(data)
    categoryTable.setRowCount(rows+1)
    categoryTable.setColumnCount(3)
    for i in range(len(header)):
        headerName = QTableWidgetItem(header[i])
        categoryTable.setItem(0, i, headerName)
        categoryTable.item(0, i).setBackground(QtGui.QColor(0, 85, 255))
        categoryTable.item(0, i).setFont(QtGui.QFont('MS Shell Dlg 2', 14))
    # categoryTable.setHorizontalHeaderLabels(header)
    for m in range(0, rows):
        operatorName = QTableWidgetItem(data.iloc[m, 0])
        fieldName = QTableWidgetItem(data.iloc[m, 1])
        text = QTableWidgetItem(str(data.iloc[m, 2]))
        categoryTable.setItem(m+1, 0, operatorName)
        categoryTable.setItem(m+1, 1, fieldName)
        categoryTable.setItem(m+1, 2, text)
        categoryTable.resizeColumnsToContents()
    categoryTable.resizeRowsToContents()
    categoryTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


class MultiLevelSortingUI(QDialog):
    def __init__(self, dataBucket):
        super(MultiLevelSortingUI, self).__init__()
        loadUi("UI\MultiLevelDialog.ui", self)
        self.dataBucket = dataBucket
        self.orderList = []
        self.Ascending = None
        self.AlgorithmNo = 0
        fillComboBox(self.SortingAlgorithmComboBox, MultiLevelAlgorithm)
        fillComboBox(self.fieldComboBox, fields)
        fillComboBox(self.OrderComboBox, ['Asc.', 'Desc.'])
        self.setWindowTitle('Multi Level Sorting')
        self.okBtn.clicked.connect(self.collectDataAndSend)
        self.addLevelBtn.clicked.connect(self.addNewLevel)
        self.delPreivouslvlBtn.clicked.connect(self.DelPreciousLvlFromList)

    def addNewLevel(self):
        self.orderList.append(fields.index(self.fieldComboBox.currentText()))
        self.updateTabel()
        self.UpdateFieldComBoBox()

    def DelPreciousLvlFromList(self):
        self.orderList.pop(len(self.orderList)-1)
        self.updateTabel()
        self.UpdateFieldComBoBox()

    def collectDataAndSend(self):
        ascending = False
        if (self.OrderComboBox.currentText() == 'Asc.'):
            ascending = True
        data = {'Algorithm': self.SortingAlgorithmComboBox.currentText(),
                'orderList': self.orderList,
                'ascending': ascending}
        self.dataBucket.storeData(data)
        self.close()

    def updateTabel(self):
        # AllItems = [self.fieldComboBox.itemText(
        #     i) for i in range(self.fieldComboBox.count())]
        # AllItems = [i for i in AllItems if (
        #     i != self.fieldComboBox.currentText())]
        # fillComboBox(self.fieldComboBox, AllItems)
        rows = len(self.orderList)
        self.showLevelsTabel.setRowCount(rows+1)
        self.showLevelsTabel.setColumnCount(1)
        m = 0
        tabelItem = QTableWidgetItem('Order')
        self.showLevelsTabel.setItem(0, 0, tabelItem)
        self.showLevelsTabel.item(0, 0).setBackground(QtGui.QColor(0, 85, 255))
        self.showLevelsTabel.item(0, 0).setFont(
            QtGui.QFont('MS Shell Dlg 2', 12))
        for i in self.orderList:
            tabelItem = QTableWidgetItem(fields[i])
            self.showLevelsTabel.setItem(m+1, 0, tabelItem)
            m += 1
        self.showLevelsTabel.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.EnabledelBtn()

    def UpdateFieldComBoBox(self):
        setOfOrderList = set([fields[x] for x in self.orderList])
        updatedFieldsList = [i for i in fields if i not in setOfOrderList]
        fillComboBox(self.fieldComboBox, updatedFieldsList)

    def EnabledelBtn(self):
        if(self.orderList == 0):
            self.delPreivouslvlBtn.setEnabled(False)
        else:
            self.delPreivouslvlBtn.setEnabled(True)


# -----------------------------------------------------------------------------------------------------------------
# -------Main Driver Code----------
if __name__ == '__main__':
    pandasData = pd.read_csv(dataFilePath)
    app = QApplication(sys.argv)
    window1 = signInUI()
    window1.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                           QtCore.Qt.WindowMinimizeButtonHint)
    window1.setWindowTitle('Sign In')
    window1.setWindowIcon(QtGui.QIcon('resources\shopping-cart (1).png'))
    window1.show()
    sys.exit(app.exec_())