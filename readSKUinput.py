import csv
import pprint
import requests
import json
import pickle
from variables import *
from datetime import datetime

file = open("sku_card_dictionary_tcgplayer.txt")
skuDictionary = json.load(file)
#pprint.pprint(skuDictionary)

onlySKU = []

for k, v in skuDictionary.items():
    for c in v:
        for d, f in c[2].items():
            onlySKU.append(d)
#pprint.pprint(onlySKU)

sku_input = ",".join(onlySKU[0:99])

url_sku = "https://api.tcgplayer.com/pricing/sku/skuIds"

headers_sku = {
    'accept': 'application/json',
    "Authorization": "bearer " + access_token
    }

skuPass = ""
skuBegin = 0
skuEnd = skuBegin + 100
resultSKU = []
count = 0

while (skuEnd <= len(onlySKU)):
    skuPass = ",".join(onlySKU[skuBegin:skuEnd])
    payload_sku = {
                #'limit': '100',
                #"categoryId": categoryId,
                #"groupId": setKey,
                "skuIds" : skuPass
                }
    response_sku = requests.request("GET", url_sku, headers=headers_sku, params=payload_sku)

    json_response_sku = json.loads(response_sku.text)
    json_response_sku_results = json_response_sku["results"]
    resultSKU.append(json_response_sku_results)
    count += 1
    print(count)
    if skuEnd == len(onlySKU):
        break
    skuBegin = skuEnd
    skuEnd = min(skuBegin + 100,len(onlySKU))
json.dump(resultSKU, open("market_pricing_12222020.txt", 'w'))
exit()

failedAppend = 0
successAppend = 0

url_price = "https://api.tcgplayer.com/pricing/marketprices/productconditionId"

headers_price = {
    'accept': 'application/json',
    "Authorization": "bearer " + access_token
    }
for k, v in skuDictionary.items():
    for c in v:
        for d, f in c[2].items():
            payload_price = {
            #'limit': '100',
            #"categoryId": categoryId,
            #"groupId": setKey,
            "productconditionId" : d
            }
            response_price = requests.request("GET", url_price, headers=headers_price, params=payload_price)

            json_response_price = json.loads(response_price.text)
            json_response_results = json_response_price["results"]
            pprint.pprint(json_response_results)
            for item in json_response_results:
                highRange = item["highestRange"]
                lowRange = item["lowestRange"]
                marketPrice = item["price"]
                try:
                    f.append([marketPrice, lowRange, highRange])
                    print("==================")
                    successAppend += 1
                    if successAppend % 1000 == 0:
                        json.dump(skuDictionary, open("pricing.txt", 'w'))
                except:
                    print("failed append")
                    failedAppend += 1

print(failedAppend)