import csv
import pprint
import requests
import json
from variables import *
from datetime import datetime
import time

logging.info(" ===== SECTION ===== ")
logging.info("Starting getSoldPrices")

# SKU dictionary contains all cards by set, product ID, and SKU ID
skuFile = open("allCardsPidSku.txt")
skuDictionary = json.load(skuFile)

# Condition and edition used to prioritize API passing order
sealedProduct = []
# [ 1st Edition, Unlimited Edition, Limited Edition ]
printingCategory = [Edition.First.value , Edition.Unl.value , Edition.Lim.value]
NM = [[], [], []]
LP = [[], [], []]
MP = [[], [], []]

logging.info("Grouping SKUs by edition/condition category")
# Removes SKUs related to Heavily Played and Damaged Cards
for product, setList in skuDictionary.items():
    for cardPrint in setList:
        skuSet = {}
        # Condition ID: 1-NM, 2-LP, 3-MP, 4-HP, 5-DMG, 6-Unopened
        # Printing ID: 7-Unl, 8-1st, 23-Limited, 102-Unopened
        # Language ID: 1-Eng
        for sku in cardPrint[2]:
            if sku["conditionId"] is not None and (sku["conditionId"] <= Condition.MP.value or sku["conditionId"] == Condition.Sealed.value):
                # Only Sealed product and singles Moderately Played and better are passed through API
                skuSet[sku["skuId"]] = [sku["conditionId"], sku["printingId"], sku["languageId"]]
                # Condition and edition batching for priority
                if sku["conditionId"] == Condition.Sealed.value:
                    sealedProduct.append(sku["skuId"])
                elif sku["conditionId"] == Condition.NM.value:
                    NM[printingCategory.index(int(sku["printingId"]))].append(sku["skuId"])
                elif sku["conditionId"] == Condition.LP.value:
                    LP[printingCategory.index(int(sku["printingId"]))].append(sku["skuId"])
                elif sku["conditionId"] == Condition.MP.value:
                    MP[printingCategory.index(int(sku["printingId"]))].append(sku["skuId"])
        cardPrint.insert(2, skuSet)
        cardPrint.pop()

onlySKU = [sealedProduct, NM[0], NM[1], NM[2], LP[0], LP[1], LP[2], MP[0], MP[1], MP[2]]

runSuccess = 0
while runSuccess != 1: # Retry logic
    try:
        # Pulls sales history data - cannot be batched, so SKUs must be requested one at a time
        # Approximate request rate is 145 requests per minute
        cardCount = 0
        successCount = 0

        # Organized as try/except to save the SKU pull spot in instances where API is not responding or other errors
        try:
            skuSold = open("skuSoldPricing.txt")
            skuSoldDictionary = json.load(skuSold)
        except:
            skuSoldDictionary = {}

        logging.info("Pulling sold prices from TCGPlayer API")
        for skuConditions in onlySKU:
            for skuIndividual in skuConditions:
                url_sku = "https://api.tcgplayer.com/pricing/marketprices/productconditionId"

                headers_sku = {
                    'accept': 'application/json',
                    "Authorization": "bearer " + access_token
                    }
                try:
                    inDictionary = skuSoldDictionary[str(skuIndividual)]
                    successCount += 1
                except:
                    payload_sku = {
                                "productconditionId" : skuIndividual
                                }

                    try:
                        response_sku_sold = requests.request("GET", url_sku, headers=headers_sku, params=payload_sku)
                    except:
                        logging.critical("Failed request: %s, %s, %s" % (url_sku, headers_sku, payload_sku))

                    json_response_sku_sold = json.loads(response_sku_sold.text)
                    json_response_results = json_response_sku_sold["results"]
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
                    if cardCount % 1000 == 0:
                        # Save spot after every 1000th iteration (roughly every 7 minutes)
                        if cardCount % 10000 == 0:
                            logging.info(cardCount)
                            logging.info("Writing data to skuSoldPricing.txt")
                        json.dump(skuSoldDictionary, open("skuSoldPricing.txt", 'w'))
        # Successfully passed every SKU
        logging.info("Writing and finalizing data to skuSoldPricing.txt")
        json.dump(skuSoldDictionary, open("skuSoldPricing.txt", 'w'))
        runSuccess = 1
    except TimeoutError:
        # Connected party did not properly respond after a period of time
        runSuccess = runSuccess - 0.01
        if runSuccess <= -10:
            exit() # Failed operation
        logging.warning("Timeout Error")
        time.sleep(35)
    except ConnectionResetError:
        # Connection forcibly closed by remote host
        runSuccess = runSuccess - 0.01
        if runSuccess <= -10:
            exit() # Failed operation
        logging.warning("Remote host closed connection")
        time.sleep(185)
    except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError):
        # Miscellaneous connection errors (e.g. remote end closed connection without response)
        runSuccess = runSuccess - 0.01
        if runSuccess <= -10:
            exit() # Failed operation
        logging.warning("Connection Error")
        time.sleep(95)
    except:
        # All other errors, maximum of 10
        logging.warning("Other Error")
        runSuccess = runSuccess - 1
        if runSuccess > -1000:
            time.sleep(65)
        else:
            # Create incomplete SKU dictionary - merge file will be able to process
            for skuConditions in onlySKU:
                for skuIndividual in skuConditions:
                    try:
                        inDictionary = skuSoldDictionary[str(skuIndividual)]
                    except:
                        skuSoldDictionary[skuIndividual] = ["Incomplete", "Incomplete", "Incomplete"]
            json.dump(skuSoldDictionary, open("skuSoldPricingIncomplete.txt", 'w'))
            logging.critical("Failed to pull every sold price")
            break