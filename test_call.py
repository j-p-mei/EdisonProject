import requests
import json

access_token = "L3QVhSKUq52p0wBULnfwGh8mISxeRBV25L9K5MPbWncQXJvnoU0zJ5vvEWxYL0fA1To2gsR4MXiSkVPufdBWX3CDbD-_U_FvFFQRvr0lFJqQgvJheD9nrr6baEgAcpHAlVAbx7OZhN87KrCCTtVcqjkf7qj9zQ9A2mjpVgFmKVdDZZ4_1DaAkhrEjgz1zB2R4JSIKFSdEN2XbY-NOvEtzckpVLJMb7VGcPU5w_T626PLFrKlZCoZ4VfGMvOcrTG7RXXZ1jTxhA23S4bUmQVAzo1cyodEzSLbTYhfKfxwcVqqjmLCfNO48xPxygP5ldTvKDsRxA"

url = "https://api.tcgplayer.com/v1.37.0/catalog/categories"


headers = {
    'Accept': 'application/json',
    'Authorization': 'bearer ' + access_token,
}

payload = {'limit': '100'}

response = requests.get(url, headers=headers, params=payload)

json_response = response.text

parsed = json.loads(json_response)

#print (json.dumps(parsed, indent=2, sort_keys=True))

'''
curl --include --request GET \
--header "Accept: application/json" \
--header "Authorization: bearer L3QVhSKUq52p0wBULnfwGh8mISxeRBV25L9K5MPbWncQXJvnoU0zJ5vvEWxYL0fA1To2gsR4MXiSkVPufdBWX3CDbD-_U_FvFFQRvr0lFJqQgvJheD9nrr6baEgAcpHAlVAbx7OZhN87KrCCTtVcqjkf7qj9zQ9A2mjpVgFmKVdDZZ4_1DaAkhrEjgz1zB2R4JSIKFSdEN2XbY-NOvEtzckpVLJMb7VGcPU5w_T626PLFrKlZCoZ4VfGMvOcrTG7RXXZ1jTxhA23S4bUmQVAzo1cyodEzSLbTYhfKfxwcVqqjmLCfNO48xPxygP5ldTvKDsRxA" 'https://api.tcgplayer.com/v1.37.0/catalog/categories'
'''

url2 = "https://api.tcgplayer.com/v1.37.0/catalog/categories/2/search"

headers2 = {
    'Accept': 'application/json',
    'content-type': "application/json",
    'Authorization': 'bearer ' + access_token,
}

#payload2 = {'limit': '100'}

r = requests.post(url2, headers=headers2)

json_response2 = r.text
parsed2 = json.loads(json_response2)

print (json.dumps(parsed2, indent=2, sort_keys=True))
