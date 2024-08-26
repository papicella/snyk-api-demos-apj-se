import argparse
import sys

import requests
import time
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
        "--scmRepo", type=str, help="SCM Repo name", required=True
    )
    parser.add_argument(
        "--scmRepoBranch", type=str, help="SCM Repo branch name", required=True
    )
    parser.add_argument(
        "--snykIntId", type=str, help="Snyk SCM Integration ID", required=True
    )
    parser.add_argument(
        "--projId", type=str, help="Snyk Project ID", required=False
    )

    return parser.parse_args()

args = parse_command_line_args()

SNYK_TOKEN = args.snykToken
GITHUB_REPO = args.scmRepo
ORG_ID = args.orgId
INTEGRATION_ID = args.snykIntId
BRANCH_NAME = args.scmRepoBranch
PROJECT_ID = args.projId

SNYK_API_URL = "https://snyk.io/api/v1"
SNYK_REST_API_URL = "https://api.snyk.io/rest"
SNYK_ISSUES_URL_BASE = "https://app.snyk.io/org"
SNYK_ISSUE_COUNT = 0




def get_org_slug():
    url = f"{SNYK_REST_API_URL}/orgs/{ORG_ID}"
    headers = {
        'Authorization': f'token {SNYK_TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.api+json'
    }
    params = {
        "version": "2024-08-22"
    }
    response = requests.get(url, headers=headers,params=params)
    org_slug =  response.json().get('data', {}).get('attributes', {}).get('slug')
    return org_slug


def call_import_api():
    url = f"{SNYK_API_URL}/org/{ORG_ID}/integrations/{INTEGRATION_ID}/import"
    headers = {
        "Authorization": f"token {SNYK_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "target": {
            "owner": GITHUB_REPO.split('/')[0],
            "name": GITHUB_REPO.split('/')[1],
            "branch": BRANCH_NAME
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    # Extract and return the Location header
    location_header = response.headers.get("Location")
    if not location_header:
        raise Exception("Location header not found in response")

    return location_header

def poll_import_status(import_status_url):
    headers = {
        "Authorization": f"token {SNYK_TOKEN}"
    }
    while True:
        response = requests.get(import_status_url, headers=headers)
        response.raise_for_status()
        status = response.json()["status"]
        if status == "complete":
            return response.json()["logs"][0]['projects']
        elif status == "failed":
            raise Exception("Import failed")
        time.sleep(10)

def check_vulnerabilities(issues):
    issue_count = 0
    for issue in issues:
        attrs = issue['attributes']
        severity = attrs['effective_severity_level']
        if severity in ["high", "critical"]:
            issue_count += 1
    return issue_count


def main():
    global SNYK_ISSUE_COUNT


    if PROJECT_ID: #only do this is PROJECT_ID is present (i.e testing etc)
        issues = get_unified_issues(ORG_ID,PROJECT_ID,SNYK_TOKEN,"false")
        issue_count = check_vulnerabilities(issues)
        if issue_count>0:
            print("Issues found - goto "+SNYK_ISSUES_URL_BASE+"/"+get_org_slug()+"/project/"+PROJECT_ID)
            SNYK_ISSUE_COUNT += issue_count
            sys.exit(1)
    else:
        status_url = call_import_api()
        projects = poll_import_status(status_url)
        for project in projects:
            project_id = project["projectId"]
            issues = get_unified_issues(ORG_ID,project_id,SNYK_TOKEN,"false")
            issue_count = check_vulnerabilities(issues)
            if issue_count>0:
                print("Issues found - goto "+SNYK_ISSUES_URL_BASE+"/"+get_org_slug()+"/project/"+project_id)
                SNYK_ISSUE_COUNT += issue_count
    if SNYK_ISSUE_COUNT >0:
        sys.exit(1)

if __name__ == "__main__":
    main()