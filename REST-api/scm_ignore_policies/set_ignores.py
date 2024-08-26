import requests
import argparse

from issues import get_unified_issues


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Snyk API Examples")
    parser.add_argument(
        "--orgId", type=str, help="The Snyk Organisation Id", required=True
    )
    parser.add_argument(
        "--snykToken", type=str, help="Snyk Token", required=True
    )
    parser.add_argument(
        "--projId", type=str, help="Snyk Project ID", required=False
    )

    return parser.parse_args()

args = parse_command_line_args()

SNYK_API_URL = "https://snyk.io/api/v1"
SNYK_REST_API_URL = "https://api.snyk.io"
SNYK_TOKEN = args.snykToken
ORG_ID = args.orgId
PROJECT_ID = args.projId


def set_ignore(project_id, issue_id):
    url = f"{SNYK_API_URL}/org/{ORG_ID}/project/{project_id}/ignore/{issue_id}"
    headers = {
        'Authorization': f'token {SNYK_TOKEN}',
        'Content-Type': 'application/json'
    }
    body = {
        "ignorePath": "",
        "reason": "",
        "reasonType": "not-vulnerable",
        "disregardIfFixable": False
    }
    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    issues = get_unified_issues(ORG_ID, PROJECT_ID, SNYK_TOKEN, "false")
    for issue in issues:
        attributes = issue["attributes"]
        issue_id = attributes["problems"][0]["id"]
        rels = issue["relationships"]
        project_id = rels["scan_item"]["data"]["id"]
        set_ignore(project_id,issue_id)

if __name__ == "__main__":
    main()