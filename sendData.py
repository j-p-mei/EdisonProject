from pymongo import MongoClient
from variables import * 
import json

logging.info(" ===== SECTION ===== " )
logging.info("Starting sendData")
client = MongoClient(uri)
db=client.CardNew

file = open("output.txt")
data = json.load(file)

logging.info("Sending data to MongoDB")
try:
    result=db.Cards.insert_one(data)
    logging.info("Successful upload")
except:
    logging.critical("Failed upload")
# Print to the console the ObjectID of the new document
