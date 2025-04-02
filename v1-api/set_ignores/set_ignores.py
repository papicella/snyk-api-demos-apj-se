import datetime
import requests
import argparse
import sys
import importlib.util

# Add the path to the REST-api directory
sys.path.append('../../REST-api')

# Dynamically import the module
spec = importlib.util.find_spec('issues_by_proj_id.issues_by_proj_id')
issues_by_proj_id = importlib.util.module_from_spec(spec)
spec.loader.exec_module(issues_by_proj_id)

# Now you can use get_unified_issues from the dynamically imported module
get_unified_issues = issues_by_proj_id.get_unified_issues

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
SNYK_TOKEN = args.snykToken
ORG_ID = args.orgId
PROJECT_ID = args.projId
EXPIRY_DAYS = 90
ALLOWED_SEVERITIES = ["low", "medium", "high"]


def set_ignore(project_id, issue_id, expiry_date):
    url = f"{SNYK_API_URL}/org/{ORG_ID}/project/{project_id}/ignore/{issue_id}"
    headers = {
        'Authorization': f'token {SNYK_TOKEN}',
        'Content-Type': 'application/json'
    }
    body = {
        "ignorePath": "",
        "reason": "",
        "reasonType": "not-vulnerable",
        "disregardIfFixable": False,
        "expires": expiry_date
    }
    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    issues = get_unified_issues(ORG_ID, PROJECT_ID, SNYK_TOKEN, "false")
    current_date = datetime.datetime.now()
    exp_date = (current_date + datetime.timedelta(days=EXPIRY_DAYS)).isoformat()
    for issue in issues:
        attributes = issue["attributes"]
        issue_id = attributes["problems"][0]["id"]
        severity = attributes['effective_severity_level']
        rels = issue["relationships"]
        project_id = rels["scan_item"]["data"]["id"]
        if severity in ALLOWED_SEVERITIES:
            set_ignore(project_id,issue_id,exp_date)

if __name__ == "__main__":
    main()