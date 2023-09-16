import requests
import json

from utils import get_default_token_path, get_token
from termcolor import colored

snyk_token_path = get_default_token_path()
snyk_token = get_token(snyk_token_path)

payload = {'version': '2023-09-14',
           'limit': '100'}

my_headers = {'Authorization': 'token ' + snyk_token, 'Accept': 'application/vnd.api+json'}
response = requests.get(f'https://api.snyk.io/rest/orgs', headers=my_headers, params=payload)

data = json.loads(response.text)

orgs = data['data']

result = len(orgs)
print(colored('Number of Snyk ORGS found - ', 'red'), result)
for org in orgs:
    print(f'ORG ID: {org["id"]} - ORG NAME: {org["attributes"]["name"]}')
