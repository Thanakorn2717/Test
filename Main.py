from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time

LINK = []
ADDRESS = []
PRICE = []

URL_ZillowClone = "https://appbrewery.github.io/Zillow-Clone/"
URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSe6YRYn2CleJ_0u7lURfzbv8TyuPhS6idkfrS6sq1bONSEV_w/viewform"

resource = requests.get(URL_ZillowClone).text

data = BeautifulSoup(resource, 'lxml')
#For address and link
data_scrapped = data.select("ul.List-c11n-8-84-3-photo-cards li a")

for item in data_scrapped:
    ADDRESS.append(item.getText().strip())
    LINK.append(item["href"])

address_list = ADDRESS[0::2]
link_list = LINK[0::2]

#For price
data_scrapped_2 = data.findAll(class_="PropertyCardWrapper__StyledPriceLine")

for item in data_scrapped_2:
    PRICE.append(item.getText().strip("+/mo"))

price_list = PRICE


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL_FORM)



#Take only first 3 items to make it easy for testing code.
address_list = address_list[0:3]
price_list = price_list[0:3]
link_list = link_list[0:3]


#All list have the same len()
for i in range(0, len(address_list)):

    time.sleep(2)
    fill = driver.find_elements(By.CSS_SELECTOR, value='.whsOnd.zHQkBf')
    fill[0].send_keys(address_list[i])
    fill[1].send_keys(price_list[i])
    fill[2].send_keys(link_list[i])

    submit = driver.find_element(By.CSS_SELECTOR, value='div.lRwqcd div')
    submit.click()

    time.sleep(1.5)
    resend = driver.find_element(By.LINK_TEXT, value='ส่งคำตอบเพิ่มอีก')
    resend.click()


driver.quit()



