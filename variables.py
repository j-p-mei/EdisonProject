import tokenOutput
import logging
from enum import Enum

access_token = tokenOutput.access_token

public = "28cde0a8-2577-4f89-a616-3fdfab78d006"
secret = "a2f65722-c646-4b22-887c-be3c19e77992"

categoryId = 2

logging.basicConfig(filename="/var/log/edisonlog.txt", format='[%(asctime)s - %(levelname)s]: %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=logging.INFO)
mongo_user = "admin"
mongo_pw = "edison"
mongo_dbname = "CL0"
uri = "mongodb+srv://%s:%s@cl0.8mlyp.mongodb.net/%s?retryWrites=true&w=majority" % (mongo_user, mongo_pw, mongo_dbname)
#client = pymongo.MongoClient(uri) 
#db = client.test

class Condition(Enum):
    NM = 1
    LP = 2
    MP = 3
    HP = 4
    DMG = 5
    Sealed = 6

class Edition(Enum):
    First = 8
    Unl = 7
    Lim = 23
    Sealed = 102