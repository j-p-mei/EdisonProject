import requests
import json
from variables import *

'''
curl --include --request GET \
--header "Accept: application/json" \
--header "Authorization: bearer " + access_token 'https://api.tcgplayer.com/v1.37.0/catalog/categories'
'''
url = "https://api.tcgplayer.com/v1.37.0/catalog/categories/2/search"

headers = {
    'Accept': 'application/json',
    'content-type': "application/json",
    'Authorization': 'bearer ' + access_token,
}

#payload2 = {'limit': '100'}

r = requests.post(url, headers=headers)

json_response = r.text
parsed = json.loads(json_response)

print (json.dumps(parsed, indent=2, sort_keys=True))