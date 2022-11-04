from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv
#                    Items Class
class Items:
    name = ""
    reviews = 0
    sold = 0
    ratings = 0.0
    actualPrice = 0
    discountedPrice = 0
    prodType = ""
    def __init__(self, name , reviews , sold, ratings,actualPrice ,discountedPrice ,prodType):
        self.name = name
        self.reviews = reviews
        self.sold = sold
        self.ratings = ratings
        self.actualPrice = actualPrice
        self.discountedPrice = discountedPrice
        self.prodType = prodType

#                    Get Items Link from a Page
def getItemsLink(soup,driver,n):
    ItemsLink = {}
    try:
        lis =  soup.find_all('li',attrs={'ae_object_type':'category'})
        productType=lis[0].find('span',{'class':'category-name'})
        productType = productType.text
    except:
        productType = "Others"
    for links in soup.find_all('a',attrs={'class':'_3t7zg _2f4Ho'}):
        i = links['href']
        ItemsLink.update({i:productType})
        if len(ItemsLink) >= n: 
            n=0
            return ItemsLink,n
    return ItemsLink,n-len(ItemsLink)

#                    Returns Soup to required functions
def getPageSourceByURL(url):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(executable_path="C:\Windows\chromedriver.exe",options = option)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content,features="html.parser")
    driver.quit()
    return soup

#                    Scroll down on a page to load new items 
def scrollDown(driver):
    driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/4);")
    time.sleep(1.5)
    driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/2);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/1.25);")
    time.sleep(1)
    return driver

#                    Open Items Link from the dictionary
def openItemsLink(dictionary):
    info = []
    lis = list(dictionary)
    for i in lis:
        a = ("https:" + i)
        soup = getPageSourceByURL(a)
        try:
            items = getItemsInfo(soup,dictionary,lis)
        except:
            items = None                
        if items != None:
            info.append(items)
    return info

#                    Store Main Category Link in a set
def storeCategoryLink(WebLink):
    CategoryLink = set()
    soup = getPageSourceByURL("https:" + WebLink)
    for link in soup.find_all('dt',attrs={'class':'cate-name'}):
        a = link.find('a')['href']
        CategoryLink.add(a)
    print("Categories")
    print(CategoryLink)
    return CategoryLink

#                    Store Sub Category Link in a set
def storeSubCategoryLink(Link):
    subcatList = set()
    temp = ""
    soup = getPageSourceByURL("https:" + Link)
    lis =  soup.find_all('li',attrs={'ae_object_type':'category'})
    if len(lis) > 1:
        for singleLi in lis:
            address=singleLi.find('a',{'target':'_self'})['href']
            if(address != temp):
                subcatList.add(address)
                temp = address
    print("SubCategory")
    print(subcatList)
    return subcatList

#                    Store Sub-Sub Category Link in a set
def storeSubSubCategoryLink(Link):
    subsubcatList = set()
    lis = set()
    soup = getPageSourceByURL("https:" + Link)
    lis =  soup.find_all('li',attrs={'ae_object_type':'category'})
    if len(lis) > 1:
        for singleLi in lis:
            try:
                address = singleLi.find('a',{'target':'_self'})['href']
                if(len(address) > 1):
                    subsubcatList.add(address)
            except:
                return None
    print("SubSubCategory")
    print(subsubcatList)
    return subsubcatList

#                    Returns and store Item info from Item's page
def getItemsInfo(soup,dictionary,prod):
    productType = dictionary[prod[0]]
    
    lis =  soup.find('div',attrs={'product-info'})
    
    #                   Product Name         
    name = lis.find('h1',attrs=('product-title-text'))
    name=name.text
    
    #                  Number of Reviews         
    reviews = lis.find('span',attrs=('product-reviewer-reviews black-link'))
    if (reviews == None):
        reviews = 0
    else:
        length = len(reviews.text)
        reviews = reviews.text[:length-8]
        
    #                   Sold Quantity         
    sold = lis.find('span',attrs=('product-reviewer-sold'))
    if (sold == None):
        sold = 0
    else:
        length = len(sold.text)
        sold = sold.text[:length-7]
    
    #                   Star Ratings         
    ratings = lis.find('span',attrs=('overview-rating-average'))
    if (ratings == None):
        ratings = 0
    else:
        ratings = ratings.text
    
    price = lis.find('div',attrs=('product-price'))
    try:
        price= price.text
    except:
        return None
    if (price == ""):
    #                   Actual Price         
        actualPrice = lis.find('span',attrs=('uniform-banner-box-discounts'))
        splitted1 = actualPrice.text.split(',')
        if len(splitted1) > 1:
            splitted1 = (splitted1[0] + splitted1[1])[4:]
            splitted2 = splitted1.split("-")
            actualPrice = splitted2[0]
            actualPrice = actualPrice[:(len(actualPrice) - 2)]
        else:
            splitted1 = (splitted1[0])[4:]
            splitted2 = splitted1.split('-')
            actualPrice = splitted2[0]
            actualPrice = actualPrice[:(len(actualPrice) - 2)]
    #                   Discounted Price         
        discountedPrice = lis.find('span',attrs=('uniform-banner-box-price'))
        splitted = discountedPrice.text.split(' ')
        if len(splitted1) > 1:
            splitted2 = splitted[1]
            splitted2 = splitted2.split(',')
            if(len(splitted2)>1):
                discountedPrice = (splitted2[0] + splitted2[1])
            else:
                discountedPrice = splitted2[0] 
        else:
            discountedPrice = splitted[1]
    else:
    #                   Actual Price         
        actualPrice = lis.find('div',attrs=('product-price-del'))
        if (actualPrice == None):
            actualPrice = 0
        else:
            splitted = actualPrice.text.split(',')
            if len(splitted) > 1:
                actualPrice = (splitted[0] + splitted[1])[4:]
            else:
                actualPrice = (splitted[0])[4:]
                tempvar = ''
                for i in actualPrice:
                    if (i != ' '):
                        tempvar = tempvar + i
                actualPrice = tempvar
    #                   Discounted Price         
        discountedPrice = lis.find('div',attrs=('product-price-current'))
        if (discountedPrice == None):
            discountedPrice = 0
        else:
            splitted = discountedPrice.text.split('/')
            splitted = splitted[0].split(',')
            if len(splitted) > 1:
                discountedPrice = (str((splitted[0])[4:]) + str(splitted[1]))
                discountedPrice = discountedPrice[:(len(discountedPrice) - 1)]
            else:
                discountedPrice = str((splitted[0])[4:])
                discountedPrice = discountedPrice[:3]
        if actualPrice == 0:
            actualPrice=discountedPrice
            discountedPrice = 0
    actualPrice = str(actualPrice)
    if sold == ' ' or sold == None or sold == '':
        sold = 0
    if reviews == ' ' or reviews == None or reviews == '':
        reviews = 0
    print(" Name ",name," Reviews: ", reviews," Sold: ",sold," Actaul ",actualPrice," discount ",discountedPrice," rating ",ratings," Type ",productType)
    WriteIntoCsv(name, productType, actualPrice, sold, discountedPrice, ratings, reviews)
    print('Another Item Stored')
    items = Items(name,reviews,sold,ratings,actualPrice,discountedPrice,productType) 
    return items
    
#                    Find total page numbers and opens every page one-by-one
def findPageNumbers(Link,n):
    ItemsLink={}
    
    driver = webdriver.Chrome(executable_path="C:\Windows\chromedriver.exe")
    driver.maximize_window()
    driver.get("https:" + Link)
    driver = scrollDown(driver)
    try:
        try:
            ItemsLink={}
            counter = n
            content = driver.page_source
            soup = BeautifulSoup(content,features="html.parser")
            a,counter = getItemsLink(soup,driver,counter)
            ItemsLink.update(a)
            a =  soup.find('div',attrs={'class':'jump-aera'})
            pageNumb =  a.text
        except:
            ItemsLink={}
            counter = n
            driver.refresh()
            driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/1.6);")
            content = driver.page_source
            time.sleep(1)
            soup = BeautifulSoup(content,features="html.parser")
            a,counter = getItemsLink(soup,driver,counter)
            ItemsLink.update(a)
            a =  soup.find('div',attrs={'class':'jump-aera'})
            pageNumb =  a.text
    except:
        try:
            ItemsLink={}
            counter = n
            driver.refresh()
            driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/1.1);")
            content = driver.page_source
            soup = BeautifulSoup(content,features="html.parser")
            a,counter = getItemsLink(soup,driver,counter)
            ItemsLink.update(a)
            a =  soup.find('div',attrs={'class':'jump-aera'})
            pageNumb =  a.text
        except:
            ItemsLink={}
            counter = n
            try:
                driver.find_element(by=By.CLASS_NAME, value='next-btn next-medium next-btn-primary law-18-dialog-yes').click()
            except:
                driver.find_element(by=By.CLASS_NAME, value='law18--btn--29ue4Ne law18--left--2XI39FE').click()
            finally:
                driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/1.6);")
                content = driver.page_source
                soup = BeautifulSoup(content,features="html.parser")
                a,counter = getItemsLink(soup,driver,counter)
                ItemsLink.update(a)
                a =  soup.find('div',attrs={'class':'jump-aera'})
                try:
                    pageNumb =  a.text
                except:
                    return None,None
    n = counter
    splitted = pageNumb.split(' ')
    TotalPages = int(splitted[1])
    for i in range(2,TotalPages):
        if len(a) <= n:
            driver = nextPage(i,driver)
            driver = scrollDown(driver)
            content = driver.page_source
            soup = BeautifulSoup(content,features="html.parser")
            a,n = getItemsLink(soup,driver,n)
            ItemsLink.update(Storetemporary(a,ItemsLink))
        else:
            break
    driver.quit()
    return ItemsLink,n

#                    Get 2 dictionaries and merge them and returns 
def Storetemporary(dictionary,itemslink):
    templist = []
    dic = dict()
    lis = list(dictionary)
    lis2 = list(itemslink)
    for i in lis:
        templist.append(i)
    for i in lis2:
        templist.append(i)
    a =  dictionary[lis[0]]
    for i in templist:
        dic.update({i:a})
    return dictionary

#                    Enters the next given page number in a textbox and clicks next button of page
def nextPage(pageNumber,driver):
    try:
        try:
            driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[3]/div/div[2]/span[3]/input').clear()
        except:
            driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/1.6);")
            driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[3]/div/div[2]/span[3]/input').clear()
    except:
        try:
            driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/1.05);")
            driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[3]/div/div[2]/span[3]/input').clear()
        except:
            return driver

    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[3]/div/div[2]/span[3]/input').send_keys(Keys.BACK_SPACE)
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[3]/div/div[2]/span[3]/input').send_keys(Keys.BACK_SPACE)
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[3]/div/div[2]/span[3]/input').send_keys(pageNumber)
    try:
        driver.find_element(by=By.CLASS_NAME, value='jump-btn').click()
    except:
        return driver
    driver.refresh()
    return driver

#                   Write's data in a csv file
def WriteIntoCsv(productName, category, actualPrice, soldQuantity, discountedPrice, rating, totalReviews):
    
    with open('data.csv', 'a',encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile,lineterminator='\n')
        writer.writerow([productName, category, actualPrice , discountedPrice , soldQuantity , rating , totalReviews]) 

#                  Main Function of scraping data. It only runs n given number of times       
def scrapDataFromALiExpress(n):
    MainCategoryLinks= set()
    SubCategory = set()
    SubSubCategory = set()
    ItemsLink = dict()
    ItemsList = set()
    MainCategoryLinks.update(storeCategoryLink("Aliexpress.com"))
    for links in MainCategoryLinks:
        SubCategory.update(storeSubCategoryLink(links))
    for links in SubCategory:
        if(links[0] != 'h'):
            a = storeSubSubCategoryLink(links)
            if(a != None):
                SubSubCategory.update(a)
    counter = n
    for links in SubSubCategory:
        if(links[0] != 'h'):
            try:
                b,counter = findPageNumbers(links,counter)
            except:
                b = None
            if(b != None):
                ItemsLink.update(b)
                ItemsList.update(openItemsLink(ItemsLink))
                #WriteLinksCsv(a)
                if(len(ItemsLink) >= n):
                    break
    return ItemsList

#                  Scraping Funtion Call
tempList = set()
tempList= scrapDataFromALiExpress(1000000)