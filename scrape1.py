import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen
url = 'https://en.wikipedia.org/wiki/Category:Cosmetics_brands'
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

brand, link, parent, owner = [], [], [], []
def get_brands(soup):
    start = soup.find_all('div', class_='mw-category-group')
    for ul in start:
        children = ul.findChildren('a')
        for child in children:
            brand.append(child.text)
            url = 'https://en.wikipedia.org{}'.format(child['href'])
            link.append(url)

get_brands(soup)

for l in link:
    html2 = urlopen(l)
    soup2 = BeautifulSoup(html2, 'html.parser')
    div = soup2.find('div', {'id':"bodyContent"})
    th = div.find('th', text='Owner')
    if th is not None:
        next = th.next_sibling
        owner.append(next.text)
    else:
        owner.append('N/A')
    a1 = div.find('a', text= 'Parent')
    if a1 is not None:
        next_e = a1.next_element.next_element
        parent.append(next_e.text)
    else:
        parent.append('N/A')

df = pd.DataFrame({'brand': brand, 'brand_link': link, 'parent_company': parent, 'owner': owner})

df.to_csv('brands.csv')
