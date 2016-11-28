import requests
from bs4 import BeautifulSoup
import re
import rethinkdb as r

def get_subcategories(url):
    soup = get_source_code(url)
    subcategories = soup.find('div', class_='nav')
    for subcat in subcategories:
        url_sub = 'test'

def get_product(url):
    url_original = url
    pagination_text = '_Desde_'
    pagination = 1
    soup = get_source_code(url)
    while True:
        print('1')
        products_list = soup.find_all('li', class_='list-view-item')
        count = 0
        for product in products_list:
            if 'padItem' in product['class']:
                continue
            else:
                count = count + 1
                product_url = product.h2.a['href']
                product_object = scrape_product(product_url)
                sold_unknown = product.find('li', class_='extra-info-sold')
                if sold_unknown is None:
                    sold = 0
                else:
                    sold_unformatted = sold_unknown.text
                    sold_formatted = int(re.sub('[^\d]', '', sold_unformatted))
                    sold = sold_formatted
                condition_unknown = product.find('li', class_='extra-info-condition')
                if condition_unknown is None:
                    condition = ""
                else:
                    condition = condition_unknown
                location = product.find('li', class_='extra-info-location').text
                product_object['sold'] = sold
                product_object['condition'] = condition
                product_object['location'] = location
                print(product_object)
                print('Product N' + str(count))
        pagination = pagination + 50
        url = url_original + pagination_text + str(pagination)
        print(url)
        soup = get_source_code(url)
        if soup.find('li', class_='list-view-item'):
            continue
        else:
            break

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

def save_rethink(final_object):
    r.connect('localhost', 28015).repl()
    r.db('test').table('products').insert(final_object).run()
