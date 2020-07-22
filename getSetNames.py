import requests
import json
import pprint
import csv

access_token = "L3QVhSKUq52p0wBULnfwGh8mISxeRBV25L9K5MPbWncQXJvnoU0zJ5vvEWxYL0fA1To2gsR4MXiSkVPufdBWX3CDbD-_U_FvFFQRvr0lFJqQgvJheD9nrr6baEgAcpHAlVAbx7OZhN87KrCCTtVcqjkf7qj9zQ9A2mjpVgFmKVdDZZ4_1DaAkhrEjgz1zB2R4JSIKFSdEN2XbY-NOvEtzckpVLJMb7VGcPU5w_T626PLFrKlZCoZ4VfGMvOcrTG7RXXZ1jTxhA23S4bUmQVAzo1cyodEzSLbTYhfKfxwcVqqjmLCfNO48xPxygP5ldTvKDsRxA"
offset = 0
count = 0
totalItems = 1
setDictionary = {}

url = "https://api.tcgplayer.com/catalog/groups"

headers = {
	'accept': 'application/json',
	"Authorization": "bearer " + access_token
	}

while (offset <= totalItems):

	payload = {
		'limit': '100',
		"categoryId":"2",
		"offset": offset
	}

	response = requests.request("GET", url, headers=headers, params=payload)

	json_response = json.loads(response.text)
	json_response_results = json_response["results"]

	if (count == 0):
		totalItems = json_response["totalItems"]
		
	for result in json_response_results:
		name = result["name"]
		groupId = result["groupId"]

		setDictionary[name] = groupId

	offset += 100
	count += 1

	#json_pretty = json.dumps(json_response, indent=2, sort_keys=True)
	#print(json_pretty)

#pprint.pprint(setDictionary)
#print ("=======")
#print (len(setDictionary))

setFile = open("setDictionary.csv", "w")

writer = csv.writer(setFile)
for key, value in setDictionary.items():
    writer.writerow([key, value])

setFile.close()