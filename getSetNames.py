import requests
import json
import pprint
import csv
from variables import *

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
#writer.write("Set,SetID")
for key, value in setDictionary.items():
    writer.writerow([key, value])
setFile.close()
