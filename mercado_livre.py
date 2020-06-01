from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
import requests
import pandas as pd

# download Chrome webdriver from https://sites.google.com/a/chromium.org/chromedriver/downloads
path = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(path)

# open website
driver.get('https://www.mercadolivre.com.br/')

# print title
print(driver.title)

# search something
search = driver.find_element_by_name('as_word')
word = input('Enter product to search: ')
search.send_keys(str(word))
search.send_keys(Keys.RETURN)

# get url of the searched page and create soup element
current_url = driver.current_url
r = requests.get(current_url)
soup = bs4.BeautifulSoup(r.text, "lxml")

productList = []
priceList = []

# scrape product names and add to list
produtos = soup.find_all('span', {'class' : 'main-title'})
for produto in produtos:
	productList.append(produto.text)

# scrape prices and add to list
prices = soup.find_all('span',{'class' : 'price__fraction'})
for price in prices:
	priceList.append(price.text)

print("Number of products: ", len(productList))
print("Number of prices: ", len(priceList))

assert len(productList) == len(priceList), \
    "Number of products and number of prices are not equal :("

# convert lists to pandas dataframe
df = pd.DataFrame({'Product Name': productList, 'Price (R$)' : priceList})
print(df)

# export dataframe to csv file
df.to_csv('results.csv', index = False)

# note
# in some cases the page might have elements that are not classified correctly, missing classes, tags, names etc.
# in these cases the script will not be able to create the dataframe due to missmatch in sizes of productList and priceList
# that's an error on the page, not on the script...


# close browser
driver.quit()