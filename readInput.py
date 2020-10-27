import csv
import pprint
import requests
import json
import pickle
from variables import *
from datetime import datetime


# Card Name, Rarity, Release Set, Group ID, Edition, Condition
cardDictionary = {}

with open('card_list.csv', newline='') as csvfile:
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

url = "https://api.tcgplayer.com/pricing/group/groupId"
access_token = access_token

headers = {
    'accept': 'application/json',
    "Authorization": "bearer " + access_token
}

pidDictionary = {}

for key in cardDictionary:
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
                'limit': '100',
                "categoryId":categoryId,
                "productName": card
            }

        response_card = requests.request("GET", url_card, headers=headers_card, params=payload_card)

        json_response_card = json.loads(response_card.text)
        json_response_card_results = json_response_card["results"]

        #pprint.pprint (json_response_card)

        for item in json_response_card_results:
             if (int(item["groupId"]) == int(setID)):
                pid = item["productId"]
                try:
                    pidDictionary[int(setDictionary[key])].append((pid, card))
                except:
                    pidDictionary[int(setDictionary[key])] = [(pid, card)]
                
#print (pidDictionary)

url_price = "https://api.tcgplayer.com/pricing/group/groupId"

headers_price = {
    'accept': 'application/json',
    "Authorization": "bearer " + access_token
    }

cardPrices = {}

for setKey in pidDictionary:  
    setID = reverseSetDictionary[str(setKey)]
    payload_price = {
    'limit': '100',
    "categoryId": categoryId,
    "groupId": setKey 
    }
    priceDictionary = {}
    response_price = requests.request("GET", url_price, headers=headers_price, params=payload_price)

    json_response_price = json.loads(response_price.text)
    json_response_results = json_response_price["results"]
    for item in json_response_results:
        pid = item["productId"]
        price = item["lowPrice"]
        edition = item["subTypeName"]
        try:
            priceDictionary[pid].append((price, edition))
        except:
            priceDictionary[pid] = [(price, edition)]   

    #print (priceDictionary)

    for item in pidDictionary[setKey]:
        pid = item[0]
        name = item[1]
        price = priceDictionary[pid]
        temp = {}
        for entry in price:
            k = entry[1]
            v = entry[0]
            temp[k] = v

        itemDict = {"set": setID,
                    "price": temp,
                    }
        try:
            cardPrices[name].append(itemDict)
        except:
            cardPrices[name] = [itemDict]
    
#pprint.pprint(cardPrices)

#Add timestamp for today
#datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

cardPrices["date"] = dt_string

json.dump(cardPrices, open("output.txt", 'w'))
#data = json.load(open("output.txt"))
