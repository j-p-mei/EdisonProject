import csv
import pprint
import requests
import json


# Card Name, Rarity, Release Set, Group ID, Edition, Condition
cardDictionary = {}

with open('card_list.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row["Card Name"]
        rarity = row['Rarity']
        set = row['Set']
        edition = row['Edition']
        condition = row['Condition']
        #print(row["Card Name"], row['Rarity'], row['Set'])
        try:
            cardDictionary[set].append((name, rarity, edition, condition))
        except:
            cardDictionary[set] = [(name, rarity, edition, condition)]

#pprint.pprint(cardDictionary)

setDictionary = {}

with open('setDictionary.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        set = row["set"]
        setID = row["setID"]
        setDictionary[set] = setID

url = "https://api.tcgplayer.com/pricing/group/groupId"
access_token = "L3QVhSKUq52p0wBULnfwGh8mISxeRBV25L9K5MPbWncQXJvnoU0zJ5vvEWxYL0fA1To2gsR4MXiSkVPufdBWX3CDbD-_U_FvFFQRvr0lFJqQgvJheD9nrr6baEgAcpHAlVAbx7OZhN87KrCCTtVcqjkf7qj9zQ9A2mjpVgFmKVdDZZ4_1DaAkhrEjgz1zB2R4JSIKFSdEN2XbY-NOvEtzckpVLJMb7VGcPU5w_T626PLFrKlZCoZ4VfGMvOcrTG7RXXZ1jTxhA23S4bUmQVAzo1cyodEzSLbTYhfKfxwcVqqjmLCfNO48xPxygP5ldTvKDsRxA"
headers = {
	'accept': 'application/json',
	"Authorization": "bearer " + access_token
}


for key in cardDictionary:

    for card in cardDictionary[key]:
        name, rarity, edition, condition = card
        payload = {
        	"limit": '100',
        	"categoryId":"2",
        	"productName": name,
        	"groupName": key
        	#"offset":99
        }

    response = requests.request("GET", url, headers=headers, params=payload)
    json_response = json.loads(response.text)
    #json_response_results = json_response["results"]
    print(json_response)
    print ("======")
