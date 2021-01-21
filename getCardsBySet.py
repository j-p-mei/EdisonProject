import csv
import pprint
import requests
import json
from variables import *
from datetime import datetime

logging.info(" ===== SECTION ===== " )
logging.info("Starting getCardsBySet")

# Sets from getSetNames.py are converted to dictionaries below
setDictionary = {}
reverseSetDictionary = {}
with open('setDictionary.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        set = row["Set"].strip()
        setID = row["SetID"]
        setDictionary[set] = setID
        reverseSetDictionary[setID] = set

logging.info("Converted setDictionary.csv into dictionary for logic")

url = "https://api.tcgplayer.com/pricing/group/groupId"

headers = {
    'accept': 'application/json',
    "Authorization": "bearer " + access_token
}

# Pulls every card (Card/Product ID) in every set in the setDictionary

everyCard = {}
emptySets = []

logging.info("Going through the reverse set dictionary")

for sets in reverseSetDictionary:
    url_card = "https://api.tcgplayer.com/catalog/products/"
    headers_set = {
        'accept': 'application/json',
        "Authorization": "bearer " + access_token,
        "includeSkus": "true"
    }
    # Offset is required because TCG Player will only show 100 (limit in the header) items per request
    offset = 0
    count = 0
    totalItems = 1

    while (offset < totalItems):
        payload_set = {
            'limit': '100',
            "categoryId": categoryId,
            "groupID": sets,
            "offset": offset
        }

        try:
            response_card = requests.request("GET", url_card, headers=headers_set, params=payload_set)
        except:
            logging.critical("failed request: %s, %s, %s" % (url, headers_set, payload_set))
        
        json_response_card = json.loads(response_card.text)
        json_response_card_results = json_response_card["results"]

        for card_in_set in json_response_card_results:
            cName = card_in_set['name']
            productID = card_in_set['productId']
            # Variable "cleanName" found in JSON results - unlikely to be required for project

            try:
                everyCard[cName].append([reverseSetDictionary[sets], productID])
            except KeyError:
                everyCard[cName] = [[reverseSetDictionary[sets], productID]]
        if count == 0:
            try:
                totalItems = json_response_card["totalItems"]
            except KeyError:
                emptySets.append([sets, reverseSetDictionary[sets]])
                break
        offset += 100
        count += 1
logging.info("Finished going through the reverse set dictionary")


json.dump(emptySets, open("emptySets.txt", 'w'))
json.dump(everyCard, open("allCardsPid.txt", 'w'))
logging.info("Dumping contents into emptySets.txt and allCardsPid.txt")