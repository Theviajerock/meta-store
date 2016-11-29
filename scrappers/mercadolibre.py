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
                sold = check_numb_element(product.find('li', class_='extra-info-sold'))
                condition = check_text_element(product.find('li', class_='extra-info-condition'))
                location = check_text_element(product.find('li', class_='extra-info-location'))
                product_object['sold'] = sold
                product_object['condition'] = condition
                product_object['location'] = location
                print(product_object)
                #save_rethink(product_object)
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
    """Function that receives a product url as parameter and extracts
    the product title and price
    """
    soup = get_source_code(url)
    title = soup.find('h1', class_='vip-title-main ').text.strip()
    #The product_title class has two spaces at the end, if something doesn't work, check this.
    price = check_numb_element(soup.find('article', class_='vip-price ch-price'), 1)
    product_object = {'url':url, 'title':title, 'price':price}
    return product_object


def get_source_code(url):
    html = requests.get(url).text
    soup_source = BeautifulSoup(html, 'html.parser')
    return soup_source


def save_rethink(final_object):
    r.connect('localhost', 28015).repl()
    r.db('test').table('products').insert(final_object).run()


def check_text_element(html_element):
    if html_element is None:
        return ""
    else:
        return html_element.text

def check_numb_element(html_element, is_price=0):
    if html_element is None:
        return 0
    elif is_price == 0:
        unformatted_number = html_element.text
        formatted_number = int(re.sub('[^\d]', '', unformatted_number))
        return formatted_number
    elif is_price == 1:
        html_unformatted = html_element.strong.text
        html_formatted = int(re.sub('[^\d]', '', html_unformatted))
        return html_formatted
