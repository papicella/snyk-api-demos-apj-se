import requests
import json
from termcolor import colored
import argparse
from utils import get_default_token_path, get_token


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Snyk API Examples")
    return parser.parse_args()


snyk_token_path = get_default_token_path()
snyk_token = get_token(snyk_token_path)

my_headers = {'Authorization': 'token ' + snyk_token, 'Content-Type': 'application/json; charset=utf-8'}
response = requests.get('https://api.snyk.io/rest/openapi', headers=my_headers)

pretty_json = json.loads(response.text)
print(colored(json.dumps(response.json(), indent=2), 'blue'))