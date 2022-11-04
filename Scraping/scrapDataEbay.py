from cgi import print_exception
from distutils.filelist import findall
from re import L
from xml.dom.minidom import Element
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import time
import requests as rq


filePath='EbayData.csv'
# def safeMoreUrlsInCsv(path,UrlLinks):
#     df = pd.read_csv('data.csv')
#     UrlLinks=UrlLinks+ df['TYPE'].values.tolist()
# def getAUdollarToPKR():
#     soup = getPageSourcebyURLThroughReq(
#         'https://www.google.com/search?q=au+dollar+into+pkr&rlz=1C1KNTJ_enPK1026PK1026&oq=au+dollar+in&aqs=chrome.2.69i57j0i512l9.4776j0j7&sourceid=chrome&ie=UTF-8')
    
#     price = soup.find('span', attrs={'class': 'DFlfde'})
#     return float(price)


# def getPageSourceByURLThroughSeleinum(url):
def getPageSourceByURL(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # driver = webdriver.Chrome('path/to/chromedriver',options=option)
    driver = webdriver.Chrome(executable_path="D:\Applications\chromedriver.exe",chrome_options=options)
    driver.get(url)
    time.sleep(2)
    pageContent = driver.page_source
    soup = BeautifulSoup(pageContent, "html.parser")
    driver.quit()
    return soup
def getPageSourcebyURLThroughReq(url):
    r=rq.get(url, 'html.parser')
    pageContent=r.text
    soup=BeautifulSoup(pageContent,"lxml")
    return soup
#               1


def getAllCaegoriesData(url):
    categories = []
    # left a  class : top-cat
    soup = getPageSourceByURL(url)
    atags = soup.find_all('a', attrs={'class': 'top-cat'})
    for a in atags:
        dataSet = {
            'Name': a.find('h2').text,
            'URL': a['href']
        }
        categories.append(dataSet)
    return categories
def getitemsLinkedSavedInfile():
    fs=open('EbayItemsLinks.txt','r')
    data=fs.read()
    links=data.split('\n')
    fs.close()
    return links
def saveListintotheFile(arr):
    fs=open('EbayItemsLinks.txt','w')
    for x in arr:
        fs.write(x+'\n')
    fs.close()

#               2


def getSubCategoryInMainCategoriesURL(url):
    subCategories = []
    soup = getPageSourceByURL(url)
    atags = soup.find_all(
        'a', attrs={'class': 'b-textlink b-textlink--sibling'})
    for a in atags:
        subCategories.append(a['href'])
    return subCategories

#               3


def getItemObjectsLink(url):
    ItemsLink = []
    soup = getPageSourceByURL(url)
    atags = soup.find_all('a', attrs={'class': 's-item__link'})
    for a in atags:
        ItemsLink.append(a['href'])
    return soup,ItemsLink

#               Move to next Page


def getPageSourceBya(currentPageSoup, attributes):
    # class = pagination__next icon-link
    # aria-label="Go to next search page"
    try:
        return currentPageSoup.find('a', attrs=attributes)['href']
    except:
        return None
    

    

#               Grasp Element
def graspTheItemDetails(url,ItemType):
    soup = getPageSourceByURL(url)
    #               Name
    displayNameContainer=soup.find('h1',{'class':'x-item-title__mainTitle'})
    name = displayNameContainer.find('span', attrs={'class': 'ux-textspans ux-textspans--BOLD'}).text

    #               Discounted PRICE
    DiscountedpriceStr = soup.find(
        'span', attrs={'itemprop':'price', 'class': 'notranslate'})
    DiscountedpriceStr = DiscountedpriceStr['content']
    price = float(DiscountedpriceStr) * 136.30

    #               Actual Price
    ActualPrice = soup.find_all('span', {'class': 'cc-ts-STRIKETHROUGH'})
    if (len(ActualPrice) == 0):
        ActualPrice = price
    else:
        ActualPrice = float(ActualPrice[0].text) * 136.30

    #               Sold items
    soldQuantity = soup.find('span', {'class': 'w2b-head'})
    
    if (soldQuantity == None):
        soldQuantity = 0
    else:
        soldQuantity=soup.find('span', {'class': 'w2b-head'}).text
        soldQuantity=[x for x in soldQuantity if ord(x) < 58 and ord(x) > 47]
        if(len(soldQuantity) > 0):
            soldQuantity = int(''.join(soldQuantity))
        else:
            soldQuantity=0
    #               Ratings
    Ratings = soup.find('span', {'class': 'ebay-review-start-rating'})
    if (Ratings == None):
        Ratings = 0
    else:
        Ratings = float(soup.find('span', {'class': 'ebay-review-start-rating'}).text)

    #               Reviews
    #   review--section
    Reviews = soup.find_all('a', {'class':'sar-btn right','rel':'nofollow'})
    if(len(Reviews) > 0):
        Reviews=[x for x in Reviews[0].text if ord(x) < 58 and ord(x) > 47]
        Reviews = int(''.join(Reviews))
    else:
        Reviews=0
    itemData = {'Name': name,
                'Price': ActualPrice,
                'Disc': price,
                'SoldItems': soldQuantity,
                'Reviews': Reviews,
                'Ratings': Ratings,
                'Type':ItemType
                }
    return itemData
def getDataFromEbay(no):
    data=[]
    soup=getPageSourceByURL('https://ebay.com')
    allcategoriesLink=soup.find('a',{'id':'gh-shop-see-all'})['href']
    
    categoriesList=getAllCaegoriesData(allcategoriesLink)
    for category in categoriesList:
        # dataSet be like ((Name:'Electronic'),(URL:'https://abc.com'))
        # dataSet[0][1] this will get the name of major category
        # dataSet[1][1] this will get the name of category url
        dataSet=list(category.items())
        UrlList=getSubCategoryInMainCategoriesURL(dataSet[1][1])
        for url in UrlList[2:]:
            itemsUrlList=getitemsLinkedSavedInfile()
            if(len(itemsUrlList) == 0):
                currentPageUrl=url
                currentSoup,items=getItemObjectsLink(currentPageUrl)
                itemsUrlList=itemsUrlList + items
                nextPageUrl= getPageSourceBya(currentSoup , {'class':'pagination__next icon-link','aria-label':'Go to next search page'})
                while(nextPageUrl != None ):
                    nextLinkSoup,nextItems=getItemObjectsLink(nextPageUrl)
                    itemsUrlList=itemsUrlList + nextItems
                    nextPageUrl= getPageSourceBya(nextLinkSoup, {'class':'pagination__next icon-link','aria-label':'Go to next search page'})
                    if len(itemsUrlList)>no :
                        break
                saveListintotheFile(itemsUrlList)
            else:
                saveListintotheFile([])
            for itemUrlLink in itemsUrlList:
                newEntry=graspTheItemDetails(itemUrlLink , dataSet[0][1])
                data.append(newEntry)
                SafeUpdatedItemsInCSV(newEntry, filePath)
                if len(data)>no :
                    break
            if len(data)>no :
                break
        if len(data)>no :
            break

def SafeUpdatedItemsInCSV(NewEntry,filePath):
    df=pd.read_csv(filePath)
    if(len(df)>0):
        names=df['Name'].values.tolist()
        ActualPrices=df['Price'].values.tolist()
        price=df['Disc'].values.tolist()
        soldQuantity=df['SoldItems'].values.tolist()
        Reviews=df['Reviews'].values.tolist()
        Ratings=df['Ratings'].values.tolist()
        ItemType=df['Type'].values.tolist()
        #           Add new items into array
        names.append(NewEntry['Name'] )
        ActualPrices.append(NewEntry['Price'] )
        price.append(NewEntry['Disc'] )
        soldQuantity.append(NewEntry['SoldItems'] )
        Reviews.append(NewEntry['Reviews'] )
        Ratings.append(NewEntry['Ratings'] )
        ItemType.append(NewEntry['Type'] )
        dataBase={'Name': names,
                'Type':ItemType,
                'Price': ActualPrices,
                'Disc': price,
                'SoldItems': soldQuantity,
                'Reviews': Reviews,
                'Ratings': Ratings
                }
        df=pd.DataFrame(data=dataBase)
    else:
        # ['Name','Type','Price','Disc','SoldItems','Reviews','Ratings'
        data={'Name': [NewEntry['Name']] ,
                    'Price': [NewEntry['Price']],
                    'Disc': [NewEntry['Disc']],
                    'SoldItems': [NewEntry['SoldItems']],
                    'Reviews': [NewEntry['Reviews']],
                    'Ratings': [NewEntry['Ratings']],
                    'Type':[NewEntry['Type']]
                    }
        df=pd.DataFrame(data)
    df.to_csv(filePath)
    print('1 more data Add')

            

data=getDataFromEbay(1000000)
# saveListintotheFile(['Https://www.google.com','Https://www.Youtube.com','Https://www.FaceBook.com','Https://www.Twitter.com','https://n/n'])
# item=(graspTheItemDetails('https://www.ebay.com/itm/304268621383?_trkparms=amclksrc%3DITM%26aid%3D777008%26algo%3DPERSONAL.TOPIC%26ao%3D1%26asc%3D20220725101321%26meid%3D8e5c8a1d0957490083032fb2eb1b2624%26pid%3D101251%26rk%3D1%26rkt%3D1%26itm%3D304268621383%26pmt%3D1%26noa%3D1%26pg%3D2380057%26algv%3DPersonalizedTopicsV2WithTopicMLR%26brand%3DForceum&_trksid=p2380057.c101251.m47269&_trkparms=pageci%3Aa77364e6-4c77-11ed-8211-5204bfbd24ea%7Cparentrq%3Adb475eda1830ab9e64171060fffed20c%7Ciid%3A1','ABC'))
# print(item)
# SafeUpdatedItemsInCSV(item, filePath)
# print(getPageSourcebyURLThroughReq ('https://www.ebay.com/?PARM3_ID=GBH_168&FF11=GBH_168&kw=6349048d6be7a10001d50951_14997&mkevt=1&mkcid=16&mkrid=711-155609-835623-2&ufes_redirect=true') )
# print(getAUdollarToPKR())



#_______________________________________________________________________________________________________________
# #_____________________________________________________________________________________________________________
# #_____________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________
#                   google colab code
# # install chromium, its driver, and selenium
# !apt-get update # to update ubuntu to correctly run apt install
# !apt install chromium-chromedriver
# !cp /usr/lib/chromium-browser/chromedriver /usr/bin
# !pip install selenium
# !pip install bs4
# !pip install webdriver-manager
# import sys
# sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
# from selenium import webdriver
  
# from cgi import print_exception
# from distutils.filelist import findall
# from re import L
# # from selenium import webdriver
# from bs4 import BeautifulSoup
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd
# import time
# import requests as rq
# # import pandas as pd #install chrom webdriver


# filePath='/content/CombineData.csv'


# def getPageSourceByURL(url):
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     driver = webdriver.Chrome('chromedriver',options=chrome_options)
#     driver.get(url)
#     time.sleep(2)
#     pageContent = driver.page_source
#     soup = BeautifulSoup(pageContent, "html.parser")
#     driver.quit()
#     return soup
# def getPageSourcebyURLThroughReq(url):
#     r=rq.get(url, 'html.parser')
#     pageContent=r.text
#     soup=BeautifulSoup(pageContent,"lxml")
#     return soup
# #               1


# def getAllCaegoriesData(url):
#     categories = []
#     # left a  class : top-cat
#     soup = getPageSourceByURL(url)
#     atags = soup.find_all('a', attrs={'class': 'top-cat'})
#     for a in atags:
#         dataSet = {
#             'Name': a.find('h2').text,
#             'URL': a['href']
#         }
#         categories.append(dataSet)
#     return categories

# #               2


# def getSubCategoryInMainCategoriesURL(url):
#     subCategories = []
#     soup = getPageSourceByURL(url)
#     atags = soup.find_all(
#         'a', attrs={'class': 'b-textlink b-textlink--sibling'})
#     for a in atags:
#         subCategories.append(a['href'])
#     return subCategories

# #               3


# def getItemObjectsLink(url):
#     ItemsLink = []
#     soup = getPageSourceByURL(url)
#     atags = soup.find_all('a', attrs={'class': 's-item__link'})
#     for a in atags:
#         ItemsLink.append(a['href'])
#     return soup,ItemsLink

# #               Move to next Page


# def getPageSourceBya(currentPageSoup, attributes):
#     # class = pagination__next icon-link
#     # aria-label="Go to next search page"
#     try:
#         return currentPageSoup.find('a', attrs=attributes)['href']
#     except:
#         return None
    

    

# #               Grasp Element
# def graspTheItemDetails(url,ItemType):
#     try:
#       soup = getPageSourceByURL(url)
#       #               Name
#       displayNameContainer=soup.find('h1',{'class':'x-item-title__mainTitle'})
#       name = displayNameContainer.find('span', attrs={'class': 'ux-textspans ux-textspans--BOLD'}).text

#       #               Discounted PRICE
#       DiscountedpriceStr = soup.find(
#         'span', attrs={'itemprop':'price', 'class': 'notranslate'})
#       DiscountedpriceStr = DiscountedpriceStr['content']
#       price = float(DiscountedpriceStr) * 136.30

#       #               Actual Price
#       ActualPrice = soup.find_all('span', {'class': 'cc-ts-STRIKETHROUGH'})
#       if (len(ActualPrice) == 0):
#           ActualPrice = price
#       else:
#         ActualPrice = float(ActualPrice[0].text) * 136.30

#     #               Sold items
#       soldQuantity = soup.find('span', {'class': 'w2b-head'})

#       if (soldQuantity == None):
#           soldQuantity = 0
#       else:
#           soldQuantity=soup.find('span', {'class': 'w2b-head'}).text
#           soldQuantity=[x for x in soldQuantity if ord(x) < 58 and ord(x) > 47]
#           soldQuantity = int(''.join(soldQuantity))
#       #               Ratings
#       #               Ratings
#       Ratings = soup.find('span', {'class': 'ebay-review-start-rating'})
#       if (Ratings == None):
#           Ratings = 0
#       else:
#           Ratings = float(soup.find('span', {'class': 'ebay-review-start-rating'}).text)
#       #               Reviews
#       #   review--section
#       Reviews = soup.find_all('a', {'class':'sar-btn right','rel':'nofollow'})
#       if(len(Reviews) > 0):
#           Reviews=[x for x in Reviews[0].text if ord(x) < 58 and ord(x) > 47]
#           Reviews = int(''.join(Reviews))
#       else:
#           Reviews=0
#       itemData = {'Name': name,
#                   'Price': ActualPrice,
#                   'Disc': price,
#                   'SoldItems': soldQuantity,
#                   'Reviews': Reviews,
#                   'Ratings': Ratings,
#                   'Type':ItemType
#                   }
#       return itemData
#     except:
#       return None

# def getDataFromEbay(no):
#     data=[]
#     soup= getPageSourceByURL('https://www.ebay.com/')
#     try:
#       allcategoriesLink=soup.find('a',{'id':'gh-shop-see-all'})['href']
#     except:  
#       allcategoriesLink='https://www.ebay.com/n/all-categories'
#     categoriesList=getAllCaegoriesData(allcategoriesLink)
#     for category in categoriesList:
#         # dataSet be like ((Name:'Electronic'),(URL:'https://abc.com'))
#         # dataSet[0][1] this will get the name of major category
#         # dataSet[1][1] this will get the name of category url
#         print('New category Url found')
#         dataSet=list(category.items())
#         UrlList=getSubCategoryInMainCategoriesURL(dataSet[1][1])
#         itemsUrlList=[]
#         for url in UrlList[2:]:
#             print('New Sub Category Url found')
#             currentPageUrl=url
#             currentSoup,items=getItemObjectsLink(currentPageUrl)
#             itemsUrlList=itemsUrlList + items
#             nextPageUrl= getPageSourceBya(currentSoup , {'class':'pagination__next icon-link','aria-label':'Go to next search page'})
            
#             while(nextPageUrl != None ):
#                 print('new Page opens')
#                 nextLinkSoup,nextItems=getItemObjectsLink(nextPageUrl)
#                 itemsUrlList=itemsUrlList + nextItems
#                 nextPageUrl= getPageSourceBya(nextLinkSoup, {'class':'pagination__next icon-link','aria-label':'Go to next search page'})
#                 if len(data)>no :
#                     break
#             for itemUrlLink in itemsUrlList:
#                 print('elements Add')
#                 newEntry=graspTheItemDetails(itemUrlLink , dataSet[0][1])
#                 if(newEntry!=None):
#                     data.append(newEntry)
#                     SafeUpdatedItemsInCSV(newEntry, filePath)
#                 if len(data)>no :
#                     break
#             if len(data)>no :
#                 break
#         if len(data)>no :
#             break

# def SafeUpdatedItemsInCSV(NewEntry,filePath):
#     df=pd.read_csv(filePath)
#     if(len(df)>0):
#         names=df['Name'].values.tolist()
#         ActualPrices=df['Price'].values.tolist()
#         price=df['Disc'].values.tolist()
#         soldQuantity=df['SoldItems'].values.tolist()
#         Reviews=df['Reviews'].values.tolist()
#         Ratings=df['Ratings'].values.tolist()
#         ItemType=df['Type'].values.tolist()
#         #           Add new items into array
#         names.append(NewEntry['Name'] )
#         ActualPrices.append(NewEntry['Price'] )
#         price.append(NewEntry['Disc'] )
#         soldQuantity.append(NewEntry['SoldItems'] )
#         Reviews.append(NewEntry['Reviews'] )
#         Ratings.append(NewEntry['Ratings'] )
#         ItemType.append(NewEntry['Type'] )
#         dataBase={'Name': names,
#                 'Type':ItemType,
#                 'Price': ActualPrices,
#                 'Disc': price,
#                 'SoldItems': soldQuantity,
#                 'Reviews': Reviews,
#                 'Ratings': Ratings
#                 }
#         df=pd.DataFrame(data=dataBase)
#     else:
#         # ['Name','Type','Price','Disc','SoldItems','Reviews','Ratings'
#         data={'Name': [NewEntry['Name']] ,
#                     'Price': [NewEntry['Price']],
#                     'Disc': [NewEntry['Disc']],
#                     'SoldItems': [NewEntry['SoldItems']],
#                     'Reviews': [NewEntry['Reviews']],
#                     'Ratings': [NewEntry['Ratings']],
#                     'Type':[NewEntry['Type']]
#                     }
#         df=pd.DataFrame(data)
#     df.to_csv(filePath)
#     print('1 more data Add')

            

# data=getDataFromEbay(50000)
# # item=(graspTheItemDetails('https://www.ebay.com/itm/284709373652?hash=item424a0046d4:g:SV4AAOSw1rJiNEu2', 'Electronic'))
# # print(item)
