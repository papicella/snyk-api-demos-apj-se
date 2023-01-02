import requests
import json
import argparse
from termcolor import colored
from utils import get_default_token_path, get_token


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Snyk API Examples")
    parser.add_argument(
        "--orgId", type=str, help="The Snyk Organisation Id", required=True
    )
    return parser.parse_args()


snyk_token_path = get_default_token_path()
snyk_token = get_token(snyk_token_path)
args = parse_command_line_args()
org_id = args.orgId

my_headers = {'Authorization': 'token ' + snyk_token, 'Content-Type': 'application/json; charset=utf-8'}
response = requests.get(f'https://snyk.io/api/v1/org/{org_id}/projects', headers=my_headers)

data = json.loads(response.text)

projects = data['projects']
OriginDict = {}

for project in projects:
    if project['origin'] not in OriginDict:
        OriginDict.update({project['origin']: 0})
    else:
        x = OriginDict[project['origin']]
        x += 1
        OriginDict.update({project['origin']: x})

print(colored(json.dumps(OriginDict, indent=2), 'blue'))
