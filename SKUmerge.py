import csv
import pprint
import requests
import json
import pickle
from variables import *
from datetime import datetime

file = open("sku_card_dictionary_tcgplayer.txt")
skuDictionary = json.load(file)

filetwo = open("market_pricing_12222020.txt")
pricingDataRaw = json.load(filetwo)
pricingData = {}

for blocks in pricingDataRaw:
    for block in blocks:
        pricingData[block["skuId"]] = block["lowestListingPrice"]
count = 0

for k, v in skuDictionary.items():
    for c in v:
        for d, f in c[2].items():
            try:
                f.append(pricingData[int(d)])
                count += 1
                print(count)
            except:
                pass

json.dump(skuDictionary, open("test_12222020.txt", 'w'))

setFile = open("test_12222020.csv", "w", newline='')
writer = csv.writer(setFile)
writer.writerow(["Set", "Card Name", "Product ID", "SKU ID", "SKU ID Details", "Price"])

for k, v in skuDictionary.items():
    for c in v:
        for d, f in c[2].items():
            if f[3] is None:
                writer.writerow([k, c[0], c[1], d, "C:" + str(f[0]) + "E:" + str(f[1]) + "L:" + str(f[2]), "N/A"])
            else:
                writer.writerow([k, c[0], c[1], d, "C:" + str(f[0]) + "E:" + str(f[1]) + "L:" + str(f[2]), f[3]])

setFile.close()