import argparse

import requests
import json
from urllib.parse import urlencode

from utils import get_default_token_path, get_token
from termcolor import colored

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Snyk API Examples")
    parser.add_argument(
        "--orgId", type=str, help="The Snyk Organisation Id", required=True
    )
    return parser.parse_args()

def listToString(s):
    str1 = ""
    if s:
        for ele in s:
            str1 += ele + " "
    return str1

snyk_token_path = get_default_token_path()
snyk_token = get_token(snyk_token_path)
args = parse_command_line_args()
org_id = args.orgId

payload = {'version': '2024-09-04',
           'limit': '100',
           'type': 'package_vulnerability'}

SNYK_REST_API_URL = 'https://api.snyk.io'

my_headers = {'Authorization': 'token ' + snyk_token, 'Accept': 'application/vnd.api+json'}
url = f"{SNYK_REST_API_URL}/rest/orgs/{org_id}/issues"
all_issues = []
url = f"{url}?{urlencode(payload)}"
count = 1;

while url:
    print(f'Getting page {count} of 100 results')
    response = requests.get(url, headers=my_headers)
    data = response.json()
    all_issues.extend(data['data'])
    next = data['links'].get('next')
    if next is None:
        break

    count += 1
    url = SNYK_REST_API_URL + next

print(f'\nAll SCA and Container issues count {len(all_issues)}')

print(colored(json.dumps(all_issues, indent=2), 'blue'))