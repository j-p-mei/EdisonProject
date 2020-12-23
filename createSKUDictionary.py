import csv
import pprint
import requests
import json
import pickle
from variables import *
from datetime import datetime

#cardDictionary = {}
newFile = open("SKUinclusion.txt")
cardDictionary = json.load(newFile)
'''
with open('allCards_pid_clean.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row["Card Name"].strip()
        set = row['Set'].strip()
        product = row['ProductID'].strip()
        try:
            cardDictionary[set].append([name, product])
        except:
            cardDictionary[set] = [[name, product]]
'''
#pprint.pprint(cardDictionary)

for product, setList in cardDictionary.items():
    for cardPrint in setList:
        skuSet = {}
        #skuSet = {SKU: [condition ID, printing ID, language ID]}
        #condition ID: 1-NM, 2-LP, 3-MP, 4-HP, 5-DMG, 6-Unopened
        #printing ID: 7-Unl, 8-1st
        #language ID: 1-Eng
        for sku in cardPrint[2]:
            skuSet[sku["skuId"]] = [sku["conditionId"], sku["printingId"], sku["languageId"]]
        cardPrint.insert(2, skuSet)
        cardPrint.pop()

pprint.pprint(cardDictionary)
json.dump(cardDictionary, open("sku_card_dictionary_tcgplayer.txt", 'w'))

exit()

cardcount = 0
setDictionary = {}
reverseSetDictionary = {}

with open('setDictionary.csv', newline='') as csvfile:
    reader2 = csv.DictReader(csvfile)
    for row in reader2:
        set = row["Set"].strip()
        setID = row["SetID"]
        setDictionary[set] = setID
        reverseSetDictionary[setID] = set

#trial = cardDictionary["Yu-Gi-Oh! ZEXAL World Duel Carnival Promos"][0][1]
#print(trial)

url_condition = "https://api.tcgplayer.com/catalog/products/productId/skus"
headers_condition = {
    'accept': 'application/json',
    "Authorization": "bearer " + access_token,
    "includeSkus":"true"
    }
#print(cardDictionary["2002 Collectors Tin"])
for set_name, card_name in cardDictionary.items():
    print(set_name)
    for printings in card_name:
        try:
            print(type(printings[2]))
            print("passin fam - list")
        except:
            payload_condition = {
                # 'limit': '100',
                "categoryId": categoryId,
                "productId": printings[1]
            }
            response_condition = requests.request("GET", url_condition, headers=headers_condition,
                                                  params=payload_condition)
            json_response_condition = json.loads(response_condition.text)
            json_response_results_condition = json_response_condition["results"]
            # pprint.pprint(json_response_results_condition)
            # Conditions: NM-1, LP-2, MP-3, HP-4
            printings.append(json_response_results_condition)
            cardcount += 1
            print(cardcount)
            if cardcount % 10 == 0:
                json.dump(cardDictionary, open("SKUinclusion.txt", 'w'))

            '''
            if type(printings[2]) == "<class 'list'>":
                print(type(printings[2]))
                print("passin fam - list")
                pass
            else:
                payload_condition = {
                    # 'limit': '100',
                    "categoryId": categoryId,
                    "productId": printings[1]
                }
                response_condition = requests.request("GET", url_condition, headers=headers_condition,
                                                      params=payload_condition)
                json_response_condition = json.loads(response_condition.text)
                json_response_results_condition = json_response_condition["results"]
                # pprint.pprint(json_response_results_condition)
                # Conditions: NM-1, LP-2, MP-3, HP-4
                printings.append(json_response_results_condition)
                json.dump(cardDictionary, open("SKUinclusion.txt", 'w'))
                cardcount += 1
                print(cardcount)
        except:
            payload_condition = {
                # 'limit': '100',
                "categoryId": categoryId,
                "productId": printings[1]
            }
            response_condition = requests.request("GET", url_condition, headers=headers_condition,
                                                  params=payload_condition)
            json_response_condition = json.loads(response_condition.text)
            json_response_results_condition = json_response_condition["results"]
            # pprint.pprint(json_response_results_condition)
            # Conditions: NM-1, LP-2, MP-3, HP-4
            printings.append(json_response_results_condition)
            #json.dump(cardDictionary, open("SKUinclusion.txt", 'w'))
            cardcount += 1
            print(cardcount)
'''
json.dump(cardDictionary, open("SKUinclusion.txt", 'w'))
exit()


url_price = "https://api.tcgplayer.com/pricing/group/groupId"

headers_price = {
    'accept': 'application/json',
    "Authorization": "bearer " + access_token,
    "includeSkus":"true"
    }

for setKey in cardDictionary:
    setID = setDictionary[str(setKey)]
    payload_price = {
    #'limit': '100',
    "categoryId": categoryId,
    "groupId": setDictionary[str(setKey)],
    "conditionId" : 1
    }
    priceDictionary = {}
    response_price = requests.request("GET", url_price, headers=headers_price, params=payload_price)

    json_response_price = json.loads(response_price.text)
    json_response_results = json_response_price["results"]
    pprint.pprint(json_response_results)
