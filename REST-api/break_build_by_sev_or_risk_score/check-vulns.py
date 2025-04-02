# check-vulns.py
import sys
import os

import requests
# Add the directory containing REST-api to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from issues.issues_by_proj_id import get_unified_issues
from import_utils import get_projects
from arg_parser import parse_command_line_args

args = parse_command_line_args()

SNYK_ISSUES_URL_BASE = "https://app.snyk.io/org"
SNYK_ISSUE_COUNT = 0


def get_org_slug():
    url = f"https://api.snyk.io/rest/orgs/{args.orgId}"
    headers = {
        'Authorization': f'token {args.snykToken}',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.api+json'
    }
    params = {
        "version": "2024-08-22"
    }
    response = requests.get(url, headers=headers, params=params)
    org_slug = response.json().get('data', {}).get('attributes', {}).get('slug')
    return org_slug


def check_vulnerabilities(issues):
            issue_count = 0
            for issue in issues:
                attrs = issue['attributes']
                if args.riskScoreThreshold:
                    risk_score = float(attrs['risk']['score']['value'])
                    if risk_score >= args.riskScoreThreshold:
                        issue_count += 1
                else:
                    severity = attrs['effective_severity_level']
                    if severity in ["high", "critical"]:
                        issue_count += 1
            return issue_count



def main():
    global SNYK_ISSUE_COUNT

    if args.projId:  # only do this if PROJECT_ID is present (i.e testing etc)
        issues = get_unified_issues(args.orgId, args.projId, args.snykToken, "false")
        issue_count = check_vulnerabilities(issues)
        if issue_count > 0:
            print("Issues found - goto " + SNYK_ISSUES_URL_BASE + "/" + get_org_slug() + "/project/" + args.projId)
            SNYK_ISSUE_COUNT += issue_count
            sys.exit(1)
    else:
        projects = get_projects(args)

        for project in projects:

            project_id = project["projectId"]
            issues = get_unified_issues(args.orgId, project_id, args.snykToken, "false")

            issue_count = check_vulnerabilities(issues)

            if issue_count > 0:
                print("Issues found - goto " + SNYK_ISSUES_URL_BASE + "/" + get_org_slug() + "/project/" + project_id)
                SNYK_ISSUE_COUNT += issue_count
    if SNYK_ISSUE_COUNT > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
