import requests
import json
import pprint
import csv
import sys
from variables import *

def main(argv):
    
    if (len(argv)>1):
        print ("Too Many Arguments")
        return

    offset = 0
    count = 0
    totalItems = 1
    setDictionary = {}

    #should look something like "setDictionary.csv"
    fileName = argv[0]

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

    setFile = open(fileName, "w", newline="")

    writer = csv.writer(setFile)
    writer.writerow(["Set","SetID"])
    for key, value in setDictionary.items():
        writer.writerow([key, value])
    setFile.close()
    return

if __name__ == "__main__":
    main(sys.argv[1:])
