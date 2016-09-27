from bs4 import BeautifulSoup
from selenium import webdriver
from scrape_pagination import scrape_products, scrape_info_product

driver = webdriver.PhantomJS()
driver.get('https://www.linio.com.co/')
url = driver.page_source
soup = BeautifulSoup(url, 'html.parser')
root_url = 'https://www.linio.com.co/'

for category in soup.find_all('div', class_='subcategory-menu'):
    category_name = category.div.a.text
    for subcategory in category.find_all('a', class_='subcategory-title')[2:]:
        subcategory_title = subcategory.text
        subcategory_url = subcategory['href']
        scrape_products(subcategory_url, scrape_info_product)
driver.quit()
