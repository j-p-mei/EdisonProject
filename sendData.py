from pymongo import MongoClient
from variables import * 
import json

client = MongoClient(uri)
db=client.CardNew

file = open("output.txt")
data = json.load(file)

#pprint(data)

result=db.Cards.insert_one(data)
#Step 4: Print to the console the ObjectID of the new document
