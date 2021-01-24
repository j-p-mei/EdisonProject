import csv
import pprint
import requests
import json
from variables import *
from datetime import datetime

logging.info(" ===== SECTION ===== ")
logging.info("Starting getMarketPrices")

# SKU dictionary contains all cards by set, product ID, and SKU ID
skuFile = open("allCardsPidSku.txt")
skuDictionary = json.load(skuFile)

logging.info("Processing SKU dictionary, removing MP-HP SKUs")
# Removes SKUs related to Heavily Played and Damaged Cards
for product, setList in skuDictionary.items():
    for cardPrint in setList:
        skuSet = {}
        # Condition ID: 1-NM, 2-LP, 3-MP, 4-HP, 5-DMG, 6-Unopened
        # Printing ID: 7-Unl, 8-1st, 23-Limited, 102-Unopened
        # Language ID: 1-Eng
        for sku in cardPrint[2]:
            # Only retains items with condition better than Moderately Played and Unopened product
            if sku["conditionId"] is not None and (sku["conditionId"] <= 3 or sku["conditionId"] == 6):
                skuSet[sku["skuId"]] = [sku["conditionId"], sku["printingId"], sku["languageId"]]
        cardPrint.insert(2, skuSet)
        # Removes remaining unnecessary/repeated SKU information
        cardPrint.pop()

# Isolates the SKUs from the dictionary
onlySKU = []

for cardName, cardSets in skuDictionary.items():
    for printings in cardSets:
        for skuKey, skuFields in printings[2].items():
            onlySKU.append(str(skuKey))

# Pulls market price data - can be batched as 200x SKUs per request (empirically tested)
url_sku = "https://api.tcgplayer.com/pricing/sku/skuIds"

headers_sku = {
    'accept': 'application/json',
    "Authorization": "bearer " + access_token
    }

# Parameters for string of SKUs to pass through in bulk
skuPass = ""
skuLength = 200
skuBegin = 0
skuEnd = skuBegin + skuLength
marketResultSKU = []

logging.info("Pulling batches of market prices from TCGPlayer API")
while (skuEnd <= len(onlySKU)):
    skuPass = ",".join(onlySKU[skuBegin:skuEnd])
    payload_sku = {
                "skuIds" : skuPass
                }
    try:
        response_sku = requests.request("GET", url_sku, headers=headers_sku, params=payload_sku)
    except:
        logging.critical("Failed request: %s, %s, %s" % (url_sku, headers_sku, payload_sku))

    json_response_sku = json.loads(response_sku.text)
    json_response_sku_results = json_response_sku["results"]

    if json_response_sku_results == []:
        logging.warning("Empty array appended - consider renewing token")

    marketResultSKU.append(json_response_sku_results)

    if skuEnd == len(onlySKU):
        break
    skuBegin = skuEnd
    skuEnd = min(skuBegin + skuLength, len(onlySKU))

logging.info("Market prices pulled, dumping into text file")
json.dump(marketResultSKU, open("skuMarketPricing.txt", 'w'))