import requests
import json

from utils import get_default_token_path, get_token
from termcolor import colored

def listToString(s):
    str1 = ""
    if s:
        for ele in s:
            str1 += ele + " "
    return str1

snyk_token_path = get_default_token_path()
snyk_token = get_token(snyk_token_path)

payload = {'version': '2024-09-04'}

my_headers = {'Authorization': 'token ' + snyk_token, 'Accept': 'application/vnd.api+json'}
response = requests.get(f'https://api.snyk.io/rest/self', headers=my_headers, params=payload)
pretty_json = json.loads(response.text)
print(colored(json.dumps(response.json(), indent=2), 'blue'))