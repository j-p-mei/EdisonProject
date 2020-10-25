import requests
import json
from variables import *

'''
This call takes in a offset and a category and gives a list of products from that catgegory.
        :param categoryId: type int -- corresponds to category of product to search
        :param groupID: type int -- corresponds to a set of the product 

        :return: JSON object
 '''

url = "https://api.tcgplayer.com/pricing/group/groupId"

headers = {
	'accept': 'application/json',
	"Authorization": "bearer " + access_token
	}

payload = {
	'limit': '100',
	"categoryId": categoryId,
	"groupId":"2582" 
}

response = requests.request("GET", url, headers=headers, params=payload)
#"productId":"35076"

json_response = json.loads(response.text)
json_response_results = json_response["results"]

for result in json_response_results:
	print (result)
	#if result["productId"] == 35076:
	#	print (json.dumps(result, indent=2, sort_keys=True))

		# Seems like condition is LP or better


# Pot of Greed ---------- productId: 35076,
# Duelist Pack: Kaiba --- groupId: 197,
