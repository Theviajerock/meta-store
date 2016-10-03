from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import rethinkdb as r

root_url = 'https://www.linio.com.co/'

def scrape_categories():
    driver = webdriver.PhantomJS()
    driver.get('https://www.linio.com.co/')
    url = driver.page_source
    soup = BeautifulSoup(url, 'html.parser')

    for category in soup.find_all('div', class_='subcategory-menu'):
        category_name = category.div.a.text
        for sub in category.find_all('a', class_='subcategory-title')[2:]:
            sub_title = sub.text
            sub_url = sub['href']
            scrape_products(sub_url, sub_title)
    driver.quit()

def scrape_products(url, sub_title):
     html = requests.get(url).text
     soup = BeautifulSoup(html, 'html.parser')
     page = 1
     while soup.find('div', class_='catalogue-product'):
         for product in soup.find_all('div', class_='catalogue-product'):
             product_url = root_url + product.div.a['href']
             product_name = product.div.a.img['alt']
         if product.div.a.img['data-lazy'].startswith('//'):
             image_url = 'https:'+product.div.a.img['data-lazy']
         else:
             image_url = product.div.a.img['data-lazy']
         scrape_info_product(product_url, product_name, image_url, url)
         page = page + 1
         html = requests.get(url + '?page=' + str(page)).text
         soup = BeautifulSoup(html, 'html.parser')

def scrape_info_product(product_url, product_name, image_url, sub_url):
    html = requests.get(product_url).text
    soup = BeautifulSoup(html, 'html.parser')
    category = soup.find_all('ol', class_='breadcrumb')[0].find_all('li')[2].a.span.text
    product_images = []
    for image in soup.find_all('div', id='image-product'):
        image_product = 'https:' + image.img['data-lazy']
        product_images.append(image_product)
    final_object = {'category-title':category, 'subcategory-link':sub_url, 'product_name':product_name, 'product_images':product_images}
    print(final_object)
    save_rethink(final_object)

def save_rethink(final_object):
    r.connect('localhost', 28015).repl()
    r.db('test').table('products').insert(final_object).run()


scrape_categories()
