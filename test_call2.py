import requests
import json


access_token = "L3QVhSKUq52p0wBULnfwGh8mISxeRBV25L9K5MPbWncQXJvnoU0zJ5vvEWxYL0fA1To2gsR4MXiSkVPufdBWX3CDbD-_U_FvFFQRvr0lFJqQgvJheD9nrr6baEgAcpHAlVAbx7OZhN87KrCCTtVcqjkf7qj9zQ9A2mjpVgFmKVdDZZ4_1DaAkhrEjgz1zB2R4JSIKFSdEN2XbY-NOvEtzckpVLJMb7VGcPU5w_T626PLFrKlZCoZ4VfGMvOcrTG7RXXZ1jTxhA23S4bUmQVAzo1cyodEzSLbTYhfKfxwcVqqjmLCfNO48xPxygP5ldTvKDsRxA"

#url = "http://api.tcgplayer.com/v1.37.0/catalog/categories"
#url = "https://api.tcgplayer.com/catalog/categories/2"
#url = "https://api.tcgplayer.com/catalog/categories/2/search/manifest"
#url = "https://api.tcgplayer.com/catalog/categories/categoryId/search"
url = "https://api.tcgplayer.com/catalog/products"

headers = {
	'accept': 'application/json',
	"Authorization": "bearer " + access_token
	}

payload = {
	'limit': '100',
	"categoryId":"2",
	"offset":"5000"
}

response = requests.request("GET", url, headers=headers, params=payload)

json_response = json.loads(response.text)
json_pretty = json.dumps(json_response, indent=2, sort_keys=True)

print(json_pretty)