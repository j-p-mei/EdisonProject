import csv
import pprint
import requests
import json
from variables import *
from datetime import datetime

skuFile = open("allCardsPidSku.txt")
skuDictionary = json.load(skuFile)

# Removes SKUs related to Heavily Played and Damaged Cards
for product, setList in skuDictionary.items():
    for cardPrint in setList:
        skuSet = {}
        #condition ID: 1-NM, 2-LP, 3-MP, 4-HP, 5-DMG, 6-Unopened
        #printing ID: 7-Unl, 8-1st, 23-Limited, 102-Unopened
        #language ID: 1-Eng
        for sku in cardPrint[2]:
            if sku["conditionId"] is not None and (sku["conditionId"] <= 3 or sku["conditionId"] == 6):
                # Only condition better than Moderately Played and Unopened product are included
                skuSet[sku["skuId"]] = [sku["conditionId"], sku["printingId"], sku["languageId"]]
        cardPrint.insert(2, skuSet)
        cardPrint.pop()

# Isolates the SKUs from the dictionary
onlySKU = []

for cardName, cardSets in skuDictionary.items():
    for printings in cardSets:
        for skuKey, skuFields in printings[2].items():
            onlySKU.append(skuKey)

# Pulls sales history data - cannot be batched, so SKUs must be requested one at a time
# Approximate request rate is 145 requests per minute
cardCount = 0
successCount = 0

#Designed as try/except to save the spot of the SKU pull in case API rejects the call
try:
    skuSold = open("skuSoldPricing.txt")  # This doesn't exist yet
    skuSoldDictionary = json.load(skuSold)
except:
    skuSoldDictionary = {}

for skuIndividual in onlySKU:
    url_sku = "https://api.tcgplayer.com/pricing/marketprices/productconditionId"

    headers_sku = {
        'accept': 'application/json',
        "Authorization": "bearer " + access_token
        }
    try:
        print(type(skuSoldDictionary[str(skuIndividual)]))
        successCount += 1
        print("success " + str(successCount))
        cardCount = successCount
    except:
        print(skuIndividual)
        payload_sku = {
                    "productconditionId" : skuIndividual
                    }

        response_sku_sold = requests.request("GET", url_sku, headers=headers_sku, params=payload_sku)

        json_response_sku_sold = json.loads(response_sku_sold.text)
        json_response_results = json_response_sku_sold["results"]
        print(json_response_results)
        if json_response_results == []:
            skuSoldDictionary[skuIndividual] = [None, None, None]
        else:
            for perResult in json_response_results:
                highRange = perResult["highestRange"]
                lowRange = perResult["lowestRange"]
                marketPrice = perResult["price"]
                skuSoldDictionary[skuIndividual] = [marketPrice, lowRange, highRange]

        cardCount += 1
        print(cardCount)
        if cardCount % 1000 == 0:
            json.dump(skuSoldDictionary, open("skuSoldPricing.txt", 'w'))

json.dump(skuSoldDictionary, open("skuSoldPricing.txt", 'w'))