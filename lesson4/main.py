import re

from pymongo import MongoClient
# from pymongo.errors import DuplicateKeyError as dke
from lxml import html
import requests
from pprint import pprint

from datetime import date

url = 'https://yandex.ru/news/'
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

# with open('page.html', 'w', encoding='utf-8') as f:
#     f.write(response.text)

html_file = ''
with open('page.html', encoding='utf-8', mode='r') as f:
    html_file = f.read()

dom = html.fromstring(html_file)

# items = dom.xpath("//h2")  все новости, потом цикл по 5 новостям
items = dom.xpath("//section[@aria-labelledby='top-heading']/div/div")

# pprint(items)

current_date = date.today()
all_news = {}

count = len(items)
for i in range(count):
    news = {}
    link = items[i].xpath("//h2/a/@href")[i]
    name = items[1].xpath("//h2/a/text()")[1]
    source = 'yandex'

    news['link'] = link
    news['name'] = name
    news['source'] = source
    news['date'] = current_date

    all_news[i] = news

pprint(all_news)

client = MongoClient('localhost', 27017)
db = client['news']
yandex = db.yandex

# try:
#     yandex.insert_many(all_news)
# except:
#     print('Ошибка добавления данных в базу')


