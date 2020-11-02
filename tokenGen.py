import requests
from variables import public,secret
import json

headers = {}

data = 'grant_type=client_credentials&client_id=%s&client_secret=%s' % (public, secret)
response = requests.post('https://api.tcgplayer.com/token', headers=headers, data=data)
t = response.json()["access_token"]

t_out = open("tokenOutput.py", "w")
t_out.write('access_token = "%s"' % str(t))
t_out.close()