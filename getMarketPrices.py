import csv
import pprint
import requests
import json
from variables import *
from datetime import datetime

skuFile = open("SKUinclusion.txt") #This input file needs to be updated to the allCardsPidSku, once it's created
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
                # Only condition better than Moderately Played and Unopened product
                skuSet[sku["skuId"]] = [sku["conditionId"], sku["printingId"], sku["languageId"]]
        cardPrint.insert(2, skuSet)
        cardPrint.pop()

# Isolates the SKUs from the dictionary
onlySKU = []

for cardName, cardSets in skuDictionary.items():
    for printings in cardSets:
        for skuKey, skuFields in printings[2].items():
            onlySKU.append(skuKey)

# Pulls market price data - can be batched as 200x SKUs per request (empirically tested)
url_sku = "https://api.tcgplayer.com/pricing/sku/skuIds"

headers_sku = {
    'accept': 'application/json',
    "Authorization": "bearer " + access_token
    }

skuPass = ""
skuLength = 200
skuBegin = 0
skuEnd = skuBegin + skuLength
marketResultSKU = []

while (skuEnd <= len(onlySKU)):
    skuPass = ",".join(onlySKU[skuBegin:skuEnd])
    payload_sku = {
                "skuIds" : skuPass
                }
    response_sku = requests.request("GET", url_sku, headers=headers_sku, params=payload_sku)

    json_response_sku = json.loads(response_sku.text)
    json_response_sku_results = json_response_sku["results"]
    marketResultSKU.append(json_response_sku_results)

    if skuEnd == len(onlySKU):
        break
    skuBegin = skuEnd
    skuEnd = min(skuBegin + skuLength, len(onlySKU))

now = datetime.now()
dt_string = now.strftime("%d.%m.%Y_%H.%M")
json.dump(marketResultSKU, open("market_pricing_" + dt_string + ".txt", 'w'))