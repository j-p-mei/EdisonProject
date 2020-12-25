import csv
import pprint
import requests
import json
from variables import *
from datetime import datetime
import time

# SKU dictionary contains all cards by set, product ID, and SKU ID
skuFile = open("allCardsPidSku.txt")
skuDictionary = json.load(skuFile)

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

# Isolates the SKUs from the dictionary
onlySKU = []

for cardName, cardSets in skuDictionary.items():
    for printings in cardSets:
        for skuKey, skuFields in printings[2].items():
            onlySKU.append(skuKey)

runSuccess = 0
while runSuccess != 1: # Retry logic
    try:
        # Pulls sales history data - cannot be batched, so SKUs must be requested one at a time
        # Approximate request rate is 145 requests per minute
        cardCount = 0
        successCount = 0

        #Designed as try/except to save the spot of the SKU pull in case API rejects the call
        try:
            skuSold = open("skuSoldPricing.txt")
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
            except:
                #print(skuIndividual)
                payload_sku = {
                            "productconditionId" : skuIndividual
                            }

                response_sku_sold = requests.request("GET", url_sku, headers=headers_sku, params=payload_sku)

                json_response_sku_sold = json.loads(response_sku_sold.text)
                json_response_results = json_response_sku_sold["results"]
                #print(json_response_results)
                if json_response_results == []:
                    # No sales data over the past 30 days available
                    skuSoldDictionary[skuIndividual] = [None, None, None]
                else:
                    for perResult in json_response_results:
                        highRange = perResult["highestRange"]
                        lowRange = perResult["lowestRange"]
                        marketPrice = perResult["price"]
                        skuSoldDictionary[skuIndividual] = [marketPrice, lowRange, highRange]

                if cardCount == 0:
                    cardCount = successCount
                cardCount += 1
                print(cardCount)
                if cardCount % 1000 == 0:
                    # Save spot after every 1000th iteration (roughly every 7 minutes)
                    json.dump(skuSoldDictionary, open("skuSoldPricing.txt", 'w'))
        # Successfully passed every SKU
        json.dump(skuSoldDictionary, open("skuSoldPricing.txt", 'w'))
        runSuccess = 1
    except TimeoutError:
        # Connected party did not properly respond after a period of time
        print("===== Timeout Error =====")
        time.sleep(10)
    except ConnectionResetError:
        # Connection forcibly closed by remote host
        print("===== Remote host closed connection =====")
        time.sleep(65)
    except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError):
        # Miscellaneous connection errors (e.g. remote end closed connection without response)
        print("===== Connection Error =====")
        time.sleep(30)
    except:
        # All other errors, maximum of 10
        runSuccess = runSuccess - 1
        if runSuccess > -10:
            time.sleep(90)
        else:
            print("Failed to pass every SKU")
            # Create incomplete SKU dictionary - merge file will be able to process
            for skuIndividual in onlySKU:
                try:
                    print(type(skuSoldDictionary[str(skuIndividual)]))
                except:
                    skuSoldDictionary[skuIndividual] = ["Incomplete", "Incomplete", "Incomplete"]
            json.dump(skuSoldDictionary, open("skuSoldPricingIncomplete.txt", 'w'))
            break