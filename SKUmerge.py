import csv
import pprint
import requests
import json
from variables import *
from datetime import datetime

logging.info(" ===== SECTION ===== " )
logging.info("Starting SKUmerge")

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
            if sku["conditionId"] is not None and (sku["conditionId"] <= 3 or sku["conditionId"] == 6):
                # Only condition better than Moderately Played and Unopened product are included
                skuSet[sku["skuId"]] = [sku["conditionId"], sku["printingId"], sku["languageId"]]
        cardPrint.insert(2, skuSet)
        cardPrint.pop()

logging.info("Merging with market prices")
# Market pricing pull (structured as a list of list of dictionaries, SKU is stored as an integer)
marketPricing = open("skuMarketPricing.txt")
marketPricingDataRaw = json.load(marketPricing)
marketPricingData = {}

for marketChunks in marketPricingDataRaw:
    for marketPoint in marketChunks:
        marketPricingData[marketPoint["skuId"]] = marketPoint["lowestListingPrice"]


# Sold pricing pull (structured as a dictionary of lists, SKU is stored as a string)
skuComplete = True
try:
    soldPricing = open("skuSoldPricing.txt")
    soldPricingData = json.load(soldPricing)
    logging.info("Merging with sold prices")
except:
    soldPricing = open("skuSoldPricingIncomplete.txt")
    soldPricingData = json.load(soldPricing)
    logging.info("Merging with sold prices (incomplete)")
    skuComplete = False

count = 0

logging.info("Producing TXT output")
# Merge card data with market and sold pricing
for setName, setList in skuDictionary.items():
    for cardName in setList:
        for skuKey, skuFields in cardName[2].items():
            try:
                skuFields.append(marketPricingData[int(skuKey)]) # Append available lowest price on TCG Player
                skuFields.append(None) # Blank space to denote separation of prices - used for investment screening later
                skuFields.append(soldPricingData[str(skuKey)][0]) # Append market price (TCG Player 30 day calc)
                skuFields.append(soldPricingData[str(skuKey)][1]) # Append lowest sold price
                skuFields.append(soldPricingData[str(skuKey)][2]) # Append highest sold price
                count += 1
            except:
                pass
# Output for MongoDB, not final - needs to be cleaned by dataCleanse
json.dump(skuDictionary, open("output_raw.txt", 'w'))
logging.info("Successfully wrote to output_raw.txt")

logging.info("Producing CSV output")
# Final output in CSV form
now = datetime.now()
dt_string = now.strftime("%Y.%m.%d")
setFile = open("output_" + dt_string + ".csv", "w", newline='')
writer = csv.writer(setFile)
writer.writerow(["Card Name", "Set", "Product ID", "SKU ID", "Condition", "Edition", "Language", "Available Lowest Price", "Buy (Y/N", "Sold Market Price", "Sold Lowest Price", "Sold Highest Price"])

# Replaces null with N/A to facilitate excel formatting
for setName, setList in skuDictionary.items():
    for cardName in setList:
        for skuKey, skuFields in cardName[2].items():
            skuBlock = [setName, cardName[0], cardName[1], skuKey]
            for items in skuFields:
                if items is None:
                    skuBlock.append("N/A")
                else:
                    skuBlock.append(items)
            writer.writerow(skuBlock)
setFile.close()
logging.info("Successfully wrote to %s" % ("output_" + dt_string + ".csv"))