import argparse
import time

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

my_headers = {'Authorization': 'Token ' + snyk_token,
              'Accept': 'application/vnd.api+json',
              'Content-Type': 'application/vnd.api+json'}

params = {'version': '2024-02-16~experimental'}

payload = {
  "data": {
    "attributes": {
      "options": {
        "integration_id": "4e4efa58-ff67-43d1-88e8-85cf36f7ca40",
        "repo_url": "https://github.com/papicella/code.ios.Vulnabank",
        "revision": "88d26ff343147f6900ea66ef42b05f8d7babffa1"
      }
    },
    "type": "test"
  }
}

SNYK_REST_API_URL = 'https://api.snyk.io'

url = f"{SNYK_REST_API_URL}/rest/orgs/{org_id}/tests"
url = f"{url}?{urlencode(params)}"

print(f"Url = {url}")

response = requests.post(url, headers=my_headers, json=payload)
pretty_json = json.loads(response.text)

print(colored(json.dumps(pretty_json, indent=2), 'blue'))

while True:
    if response.status_code == 201:
        data = response.json()
        test_reference = data['links'].get('self').get('href')
        break;

print(f"HREF is {test_reference}")

my_headers = {'Authorization': 'Token ' + snyk_token}

url_no_params = test_reference.split('?')[0]

url = f'{SNYK_REST_API_URL}{test_reference}'

response = requests.get(url, headers=my_headers)
response.raise_for_status()

while True:
    data = response.json()
    state = data['data'].get('attributes').get('state')
    print(f"State = {state}")
    if state == "completed":
        pretty_json = json.loads(response.text)
        print(colored(json.dumps(response.json(), indent=2), 'blue'))
        data = response.json()
        findings_url = data['data'].get('attributes').get('findings').get('findings_url')
        findings_format = data['data'].get('attributes').get('findings').get('format')
        print(f"Format: {findings_format}, URL: {findings_url}")
        break;
    else:
        pretty_json = json.loads(response.text)
        print(colored(json.dumps(response.json(), indent=2), 'blue'))
        print('....')
        time.sleep(10)
