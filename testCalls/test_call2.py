'''
This call takes in a offset and a category and gives a list of products from that catgegory.
        :param categoryId: type int -- corresponds to category of product to search
        :param offset: type int -- index of starting point 

        :return: JSON object
'''
import requests
import json
from variables import *

url = "https://api.tcgplayer.com/catalog/products"

headers = {
    'accept': 'application/json',
    "Authorization": "bearer " + access_token
    }

payload = {
    "categoryId": categoryId,
    "offset":3
}

# Category ID is hard coded to 2 for yugioh -- this can change in the future to import from variables
# Starting at offset 5000 for testing.

response = requests.request("GET", url, headers=headers, params=payload)

json_response = json.loads(response.text)
json_pretty = json.dumps(json_response, indent=2, sort_keys=True)

print(json_pretty)