import json
import argparse
import requests
from termcolor import colored
from utils import get_default_token_path, get_token

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Snyk API Examples")
    parser.add_argument(
        "--orgId", type=str, help="The Snyk Organisation Id", required=True
    )
    parser.add_argument(
        "--projectId", type=str, help="The project ID in Snyk", required=True
    )
    return parser.parse_args()


snyk_token_path = get_default_token_path()
snyk_token = get_token(snyk_token_path)
args = parse_command_line_args()
org_id = args.orgId
project_id = args.projectId

payload = {'version': '2022-04-06~experimental',
           'format': 'cyclonedx+json'}
my_headers = {'Authorization': 'token ' + snyk_token, 'Accept': 'application/vnd.api+json'}

print(f'https://api.snyk.io/rest/orgs/{org_id}/projects/{project_id}/sbom')

response = requests.get(f'https://api.snyk.io/rest/orgs/{org_id}/projects/{project_id}/sbom',
                         headers=my_headers,
                         params=payload)

pretty_json = json.loads(response.text)
print(colored(json.dumps(response.json(), indent=2), 'blue'))
