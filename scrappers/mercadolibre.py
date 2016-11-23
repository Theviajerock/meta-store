import requests
from bs4 import BeautifulSoup
import re

def get_product(url):
    soup = get_source_code(url)
    products_list = soup.find_all('li', class_='list-view-item')
    for product in products_list:
        if 'padItem' in product['class']:
            continue
        else:
            product_url = product.h2.a['href']
            product_object = scrape_product(product_url)
            sold_unknown = product.find('li', class_='extra-info-sold')
            if sold_unknown is None:
                sold = 0
            else:
                sold_unformatted = sold_unknown.text
                sold_formatted = int(re.sub('[^\d]', '', sold_unformatted))
                sold = sold_formatted
            condition = product.find('li', class_='extra-info-condition').text
            location = product.find('li', class_='extra-info-location').text
            product_object['sold'] = sold
            product_object['condition'] = condition
            product_object['location'] = location
            print(product_object)



def scrape_product(url):
    soup = get_source_code(url)
    #The product_title class has two spaces at the end, if something doesn't work, check this.
    title = soup.find('h1', class_='vip-title-main ').text.strip()
    price_unformatted = soup.find('article', class_='vip-price ch-price').strong.text
    price = int(re.sub('[^\d]', "", price_unformatted))
    product_object = {'url':url, 'title':title, 'price':price}
    return product_object

def get_source_code(url):
    html = requests.get(url).text
    soup_source = BeautifulSoup(html, 'html.parser')
    return soup_source
