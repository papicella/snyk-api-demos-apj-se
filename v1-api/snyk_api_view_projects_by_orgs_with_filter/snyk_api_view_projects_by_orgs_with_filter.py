import requests
import json
import sys
import argparse
from utils import get_default_token_path, get_token


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Snyk API Examples")
    parser.add_argument(
        "--orgId", type=str, help="The Snyk Organisation Id", required=True
    )
    parser.add_argument(
        "--origin", type=str, help="The Origin String for the imported project , ie: github", required=True
    )
    return parser.parse_args()

snyk_token_path = get_default_token_path()
snyk_token = get_token(snyk_token_path)
args = parse_command_line_args()
org_id = args.orgId
origin = args.origin

filter_data = """{
    "filters": {
        "origin": "%s"
      }
  }""" % origin

my_headers = {'Authorization': 'token ' + snyk_token, 'Content-Type': 'application/json; charset=utf-8'}
response = requests.post(f'https://snyk.io/api/v1/org/{org_id}/projects',
                         headers=my_headers,
                         data=filter_data)
pretty_json = json.loads(response.text)
print(json.dumps(response.json(), indent=4))
