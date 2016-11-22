import requests
from bs4 import BeautifulSoup
import re

def scrape_product(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    #The product_title class has two spaces at the end, if something doesn't work, check this.
    title = soup.find('h1', class_='vip-title-main ').text.strip()
    location = soup.find('div', class_='vip-section-header').dd.span.text
    price_unformatted = soup.find('article', class_='vip-price ch-price').strong.text
    price = int(re.sub('[^\d]', "", price_unformatted))
    condition = soup.find('div', class_='item-conditions').find('dd').text.strip()
    selled_unformatted = soup.find('div', class_='item-conditions').find_all('dd')[1].text
    selled = int(re.sub('[^\d]', "", selled_unformatted))
    product_object = {'url':url, 'title':title, 'location':location, 'price':price, 'condition':condition, 'selled':selled}
    return product_object
