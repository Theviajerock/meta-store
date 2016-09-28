from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from scrape_pagination import scrape_products, scrape_info_product

root_url = 'https://www.linio.com.co/'

def scrape_categories(scraper_products, scrape_info_product):
    driver = webdriver.PhantomJS()
    driver.get('https://www.linio.com.co/')
    url = driver.page_source
    soup = BeautifulSoup(url, 'html.parser')

    for category in soup.find_all('div', class_='subcategory-menu'):
        category_name = category.div.a.text
        for subcategory in category.find_all('a', class_='subcategory-title')[2:]:
            subcategory_title = subcategory.text
            subcategory_url = subcategory['href']
            scrape_products(subcategory_url, scrape_info_product)
    driver.quit()

def scrape_products(url, scrape_info_product):
     html = requests.get(url).text
     soup = BeautifulSoup(html, 'html.parser')
     page = 1
     while soup.find('div', class_='catalogue-product'):
         for product in soup.find_all('div', class_='catalogue-product'):
             product_url = root_url + product.div.a['href']
             product_name = product.div.a.img['alt']
         if product.div.a.img['data-lazy'].startswith('//'):
             image_url = 'https:'+product.div.a.img['data-lazy']
             print(image_url)
         else:
             image_url = product.div.a.img['data-lazy']
         scrape_info_product(product_url)
         page = page + 1
         html = requests.get(url + '?page=' + str(page)).text
         soup = BeautifulSoup(html, 'html.parser')

def scrape_info_product(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    product_images = []
    for image in soup.find_all('div', id='image-product'):
        image_url = 'https:' + image.img['data-lazy']
        product_images.append(image_url)
    print(product_images)


scrape_categories(scrape_products, scrape_info_product)
