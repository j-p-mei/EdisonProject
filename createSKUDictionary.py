import csv
import pprint
import requests
import json
from variables import *
from datetime import datetime
import time

logging.info(" ===== SECTION ===== " )
logging.info("Starting createSKUDictionary")

runSuccess = 0
while runSuccess != 1: # Retry logic
    try:
        # Designed as try/except to save the spot of the SKU pull in case API rejects the call
        try:
            newFile = open("allCardsPidSku.txt")
            cardDictionary = json.load(newFile)
        except:
            cardDictionary = json.load(open("allCardsPid.txt"))

        setDictionary = {}
        reverseSetDictionary = {}

        logging.info("Loading set dictionary from csv")
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
            for printings in set_name:
                try:
                    # Check if already in the SKU list - skip if yes and call API to append if no
                    inDictionary = type(printings[2])
                    successCount += 1
                    cardCount = successCount
                except:
                    payload_condition = {
                        "categoryId": categoryId,
                        "productId": printings[1]
                    }

                    try:
                        response_condition = requests.request("GET", url_condition, headers=headers_condition, params=payload_condition)
                    except:
                        logging.critical("Failed request: %s, %s, %s" % (url_condition, headers_condition, payload_condition))

                    json_response_condition = json.loads(response_condition.text)
                    json_response_results_condition = json_response_condition["results"]
                    # Conditions: NM-1, LP-2, MP-3, Unopened-6
                    printings.append(json_response_results_condition)
                    cardCount += 1

                    if cardCount % 1000 == 0:
                        if cardCount % 10000 == 0:
                            logging.info("Writing data to allCardsPidSku.txt")
                        json.dump(cardDictionary, open("allCardsPidSku.txt", 'w'))

        # Successfully created pulled all SKU data
        logging.info("Writing and finalizing data to allCardsPidSku.txt")
        json.dump(cardDictionary, open("allCardsPidSku.txt", 'w'))
        runSuccess = 1
        logging.info("SKU dictionary creation success")
    except TimeoutError:
        # Connected party did not properly respond after a period of time
        logging.warning("Timeout Error")
        time.sleep(10)
    except ConnectionResetError:
        # Connection forcibly closed by remote host
        logging.warning("Remote Host Closed Connection")
        time.sleep(65)
    except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError):
        # Miscellaneous connection errors (e.g. remote end closed connection without response)
        logging.warning("Connection Error")
        time.sleep(30)
    except:
        # All other errors, maximum of 100
        logging.warning("Other Error")
        runSuccess = runSuccess - 1
        if runSuccess > -100:
            time.sleep(90)
        else:
            # Create incomplete SKU dictionary - no protocol in place yet to process incomplete data
            json.dump(skuSoldDictionary, open("allCardsPidSku.txt", 'w'))
            logging.critical("Failed to pull every SKU")
            break