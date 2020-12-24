import csv
import pprint
import requests
import json
from variables import *
from datetime import datetime

#Designed as try/except to save the spot of the SKU pull in case API rejects the call
try:
    newFile = open("allCardsPidSku.txt")
    cardDictionary = json.load(newFile)
except:
    cardDictionary = json.load(open("allCardsPid.txt"))

setDictionary = {}
reverseSetDictionary = {}

with open('setDictionary.csv', newline='') as csvfile:
    reader2 = csv.DictReader(csvfile)
    for row in reader2:
        set = row["Set"].strip()
        setID = row["SetID"]
        setDictionary[set] = setID
        reverseSetDictionary[setID] = set

cardCount = 0
successCount = 0

url_condition = "https://api.tcgplayer.com/catalog/products/productId/skus"

headers_condition = {
    'accept': 'application/json',
    "Authorization": "bearer " + access_token,
    "includeSkus":"true"
    }

for card_name, set_name in cardDictionary.items():
    #print(card_name)
    for printings in set_name:
        try:
            # Check if already in the SKU list - skip if yes and call API to append if no
            print(type(printings[2]))
            successCount += 1
            print("success " + str(successCount))
            cardCount = successCount
        except:
            payload_condition = {
                "categoryId": categoryId,
                "productId": printings[1]
            }
            response_condition = requests.request("GET", url_condition, headers=headers_condition, params=payload_condition)
            json_response_condition = json.loads(response_condition.text)
            json_response_results_condition = json_response_condition["results"]
            # Conditions: NM-1, LP-2, MP-3, Unopened-6
            printings.append(json_response_results_condition)
            cardCount += 1
            print(cardCount)
            if cardCount % 1000 == 0:
                json.dump(cardDictionary, open("allCardsPidSku.txt", 'w'))

json.dump(cardDictionary, open("allCardsPidSku.txt", 'w'))
