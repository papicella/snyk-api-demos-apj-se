import argparse

import requests
import json

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

payload = {'version': '2023-09-14',
           'limit': '100',
           'types': 'sast'}

my_headers = {'Authorization': 'token ' + snyk_token, 'Accept': 'application/vnd.api+json'}
response = requests.get(f'https://api.snyk.io/rest/orgs/{org_id}/projects', headers=my_headers, params=payload)

data = json.loads(response.text)
projects = data['data']

result = len(projects)
print(colored(f'Number of projects found - {result}', 'red'))
print(colored('Name,Type,Origin', 'blue'))
for project in projects:
    org_attribites = project["attributes"]
    print(f'{org_attribites["name"]},{org_attribites["type"]},{org_attribites["origin"]}')