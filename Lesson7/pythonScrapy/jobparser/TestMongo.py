from pymongo import MongoClient
import pprint


client = MongoClient('localhost', 27017)

vacancy = client.vacancyAnalyst

test_find = vacancy.find({})

for doc in vacancy.find({}):
    pprint(doc)