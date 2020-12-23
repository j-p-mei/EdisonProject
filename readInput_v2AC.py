import csv
import pprint
import requests
import json
from variables import *
from datetime import datetime


# Card Name, Rarity, Release Set, Group ID, Edition, Condition
cardDictionary = {}

with open('card_list_OG.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row["Card Name"].strip()
        set = row['Set'].strip()
        try:
            cardDictionary[set].append(name)
        except:
            cardDictionary[set] = [name]

#pprint.pprint(cardDictionary)

setDictionary = {}
reverseSetDictionary = {}

with open('setDictionary.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        set = row["Set"].strip()
        setID = row["SetID"]
        setDictionary[set] = setID
        reverseSetDictionary[setID] = set
#pprint.pprint(setDictionary)
#pprint.pprint(reverseSetDictionary)


url = "https://api.tcgplayer.com/pricing/group/groupId"

headers = {
    'accept': 'application/json',
    "Authorization": "bearer " + access_token
}
#pprint.pprint(setDictionary)
#exit()

'''emptysets = []
everyCard = {}

for sets in reverseSetDictionary:
    url_card = "https://api.tcgplayer.com/catalog/products/"
    headers_set = {
        'accept': 'application/json',
        "Authorization": "bearer " + access_token,
        "includeSkus": "true"
    }

    payload_set = {
        'limit': '100',
        "categoryId": categoryId,
        "groupID": sets
    }

    response_card = requests.request("GET", url_card, headers=headers_set, params=payload_set)
    json_response_card = json.loads(response_card.text)
    json_response_card_results = json_response_card["results"]

    for card_in_set in json_response_card_results:
        cName = card_in_set['name']
        productID = card_in_set['productId']
        #cGroup = card_in_set['groupId']
        #clName = card_in_set['cleanName']

        try:
            try:
                everyCard[cName].append([reverseSetDictionary[sets], productID])
                print(cName)
                print(everyCard[cName])
                print("******************************************************")
            except KeyError:
                everyCard[cName] = [[reverseSetDictionary[sets], productID]]
                print(cName)
                #print(sets)
                #print(reverseSetDictionary[sets])
                print(everyCard[cName])
                print("======================================================")
        except:
            emptysets.append(sets)

#EMPTYSETS FROM TCGPLAYER

pprint.pprint(emptysets)
emptysets2 = []
for es in emptysets:
    emptysets2.append(reverseSetDictionary[es])
pprint.pprint(emptysets)
pprint.pprint(emptysets2)
'''

'''json.dump(everyCard, open("everycard_pid.txt", 'w'))
data = json.load(open("everycard_pid.txt"))
exit()
'''

pidDictionary = {}

file = open("everycard_pid.txt")
allCards = json.load(file)

pprint.pprint(allCards)

for cardName, setData in allCards.items():
    print(cardName)
    print(setData)
    print("###############################")
    for indSet in setData:
        try:
            pidDictionary[setDictionary[indSet[0]]].append((indSet[1], cardName))
            print("=============================")
        except:
            pidDictionary[setDictionary[indSet[0]]] = [(indSet[1], cardName)]
#exit()
'''for key in cardDictionary:
    setID = setDictionary[key]
    #print (cardDictionary[key])
    for card in cardDictionary[key]:
        # we need the productID for each card
        url_card = "https://api.tcgplayer.com/catalog/products/"
        headers_card = {
            'accept': 'application/json',
            "Authorization": "bearer " + access_token,
            "includeSkus":"true"
            }

        payload_card = {
                #'limit': '100',
                "categoryId":categoryId,
                "productName": card
            }

        response_card = requests.request("GET", url_card, headers=headers_card, params=payload_card)

        json_response_card = json.loads(response_card.text)
        json_response_card_results = json_response_card["results"]
        print(json_response_card)
        #print(json_response_card_results)

        for item in json_response_card_results:
             if (int(item["groupId"]) == int(setID)):
                pid = item["productId"]
                try:
                    pidDictionary[int(setDictionary[key])].append((pid, card))
                except:
                    pidDictionary[int(setDictionary[key])] = [(pid, card)]
                
pprint.pprint (pidDictionary)'''

url_price = "https://api.tcgplayer.com/pricing/group/groupId"

headers_price = {
    'accept': 'application/json',
    "Authorization": "bearer " + access_token
    }

cardPrices = {}

for setKey in pidDictionary:  
    setID = reverseSetDictionary[str(setKey)]
    payload_price = {
    #'limit': '100',
    "categoryId": categoryId,
    "groupId": setKey 
    }
    priceDictionary = {}
    response_price = requests.request("GET", url_price, headers=headers_price, params=payload_price)

    json_response_price = json.loads(response_price.text)
    json_response_results = json_response_price["results"]
    #pprint.pprint(json_response_results)
    for item in json_response_results:
        pid = item["productId"]
        price = item["lowPrice"]
        edition = item["subTypeName"]
        try:
            priceDictionary[pid].append((price, edition))
        except:
            priceDictionary[pid] = [(price, edition)]

    pprint.pprint (priceDictionary)

    for item in pidDictionary[setKey]:
        pid = item[0]
        name = item[1].replace(".","")
        try:
            price = priceDictionary[pid]
            temp = {}
            for entry in price:
                k = entry[1]
                v = entry[0]
                temp[k] = v
                print(price)
        except:
            # No value stored - out of stock
            temp = {}
            temp ["Out of Stock"] = "Out of Stock"

        '''itemDict = {"set": setID,
                    "price": temp,
                    }
        '''
        try:
            cardPrices[name][setID] = temp
        except:
            cardPrices[name] = {}
            cardPrices[name][setID] = temp
    
#pprint.pprint(cardPrices)

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y_%H:%M:%S")

setFile = open("cardPrices_12202020.csv", "w")

writer = csv.writer(setFile)
for cardKey, cValue in cardPrices.items():
    for setKey, sValue in cValue.items():
        for editionKey, priceValue in sValue.items():
            writer.writerow([cardKey, setKey, editionKey, priceValue])
setFile.close()

#Add timestamp for today
#datetime object containing current date and time

cardPrices["date"] = dt_string

json.dump(cardPrices, open("output.txt", 'w'))
data = json.load(open("output.txt"))