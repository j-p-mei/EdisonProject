import requests
import json
import pprint
import csv
import sys
import logging
from variables import *

logging.info(" ===== SECTION ===== " )
logging.info("Starting getSetNames")

def main(argv):
    
    if (len(argv)>1):
        logging.critical("Too Many Arguments")
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

    
    logging.info("Hitting tcgplayer api for list of sets")
    while (offset <= totalItems):

        payload = {
            'limit': '100',
            "categoryId":"2",
            "offset": offset
        }
        try:
            response = requests.request("GET", url, headers=headers, params=payload)
        except:
            logging.critical("failed request: %s, %s, %s" % (url, headers, payload))

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

    logging.info("Finished collecting list of sets")
    logging.info("Writing collection of sets to file %s" % (fileName))
    
    setFile = open(fileName, "w", newline="")
    writer = csv.writer(setFile)
    writer.writerow(["Set","SetID"])
    for key, value in setDictionary.items():
        writer.writerow([key, value])
    setFile.close()
    logging.info("Finished writing collection of sets to file %s" % (fileName))
    return

if __name__ == "__main__":
    main(sys.argv[1:])
