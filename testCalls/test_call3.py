import requests
import json
from variables import *

url = "https://api.tcgplayer.com/catalog/products/"

headers = {
	'accept': 'application/json',
	"Authorization": "bearer " + access_token,
	"includeSkus":"true"
	}

payload = {
	'limit': '100',
	"categoryId":"2",
	"productName":"Solemn Judgment",
}

response = requests.request("GET", url, headers=headers, params=payload)

json_response = json.loads(response.text)
json_pretty = json.dumps(json_response, indent=2, sort_keys=True)

print(json_pretty)