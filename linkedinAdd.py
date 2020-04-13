import requests

client_id = '780emu22h2tfo7'
client_secret = 'kCrio5URmm6tX8KF'

payload = {'response_code': 'code', 'state': 'DCEef45A53sdfKef424', 'grant_type': 'client_credentials',
           'client_id': client_id, 'client_secret': client_secret}

r = requests.post('https://www.linkedin.com/oauth/v2/accessToken', params=payload)

print(r.json())