# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from datetime import date
import re
import pprint


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancyAnalyst

    def process_item(self, item, spider):
        print()
        #print(item)
        if spider.name == 'hhru':
            item_test = {}
            print()
            item_test['salary_min'], item_test['salary_max'], item_test['currency'] = self.process_salary(item['salary'])
            item_test['name'] = item['name']
            item_test['url'] = item['url']
            item_test['_id'] = item['url'].split('?')[0].split('/')[-1]
            #print(item_test)
        elif spider.name == 'sjru':
            print()
            item_test = {}
            item_test['name'] = item['name']
            item_test['url'] = item['url']
            item_test['salary_min'], item_test['salary_max'], item_test['currency'] = self.process_salary_job(item['salary'])
            #print()
            item_test['_id'] = re.findall('\d+', item['url'])

        item_test['date'] = date.today()
        print()
        collection = self.mongobase[spider.name]
        collection.insert_one(item_test)

        return item



    def process_salary(self, salary):
         spisok = ['от ', ' до ', 'руб.', 'з/п не указана']
         for i in spisok:
             if i in salary:
                 index = salary.index(i)
                 if i == 'от ':
                     minv = int("".join(salary[index + 1].split()))
                 elif i == ' до ':
                     maxv = int("".join(salary[index + 1].split()))
                 elif i == 'руб.':
                     cur = i
                 elif i == 'з/п не указана':
                     minv = 0
                     maxv = 0
                     cur = None
         return minv, maxv, cur

    def process_salary_job(self, salary):
        print()
        minv = 0
        maxv = 0
        cur = ''
        if len(salary) == 3:
            num = "".join(salary[0].split())
            minv = num
            maxv = num
            cur = "".join(salary[3].split())
        if  len(salary) == 4:
            minv = "".join(salary[0].split())
            maxv = "".join(salary[1].split())
            cur = "".join(salary[3].split())
        if  len(salary) == 1:
            if 'По договорённости' in salary:
                minv = 0
                maxv = 0
            if 'от' in salary:
                minv = "".join(salary[0].split())

        return  minv, maxv, cur


