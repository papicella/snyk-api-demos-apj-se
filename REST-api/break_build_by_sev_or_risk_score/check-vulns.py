# check-vulns.py
import sys
import os

import requests

from issues_by_proj_id import get_unified_issues
from import_utils import get_projects
from arg_parser import parse_command_line_args
from arg_parser import SEVERITY_LEVELS

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


def check_vulnerabilities(issues,org_slug,project_id):
    issue_count = 0
    for issue in issues:
        attrs = issue['attributes']
        #print issue url
        issue_url = get_issue_url(attrs,org_slug,project_id)
        print(issue_url)
        if args.riskScoreThreshold:
            risk_score = float(attrs['risk']['score']['value'])
            if risk_score >= args.riskScoreThreshold:
                issue_count += 1
        else:
            if not args.severityThreshold:
                severity_threshold = "high" ## default to high
            else:
                severity_threshold = args.severityThreshold.lower()

            threshold_index = SEVERITY_LEVELS.index(severity_threshold)
            for issue in issues:
                severity = issue['attributes']['effective_severity_level']
                if SEVERITY_LEVELS.index(severity) >= threshold_index:
                    issue_count += 1
    return issue_count

def main():
    global SNYK_ISSUE_COUNT

    org_slug = get_org_slug()

    if args.projId:  # only do this if PROJECT_ID is present (i.e testing etc)
        issues = get_unified_issues(args.orgId, args.projId, args.snykToken, "false")
        issue_count = check_vulnerabilities(issues,org_slug, args.projId)
        if issue_count > 0:
            print("Issues found - goto " + SNYK_ISSUES_URL_BASE + "/" + org_slug + "/project/" + args.projId)
            SNYK_ISSUE_COUNT += issue_count
            sys.exit(1)
    else:
        projects = get_projects(args)

        for project in projects:

            project_id = project["projectId"]
            issues = get_unified_issues(args.orgId, project_id, args.snykToken, "false")

            issue_count = check_vulnerabilities(issues,org_slug, project_id)

            if issue_count > 0:
                print("Issues found - goto " + SNYK_ISSUES_URL_BASE + "/" + org_slug + "/project/" + project_id)
                SNYK_ISSUE_COUNT += issue_count
    if SNYK_ISSUE_COUNT > 0:
        sys.exit(1)


def get_issue_url(issue,org_slug, project_id):
    #example URL https://app.snyk.io/org/lawrence_crowther_hmv/project/9d4b653f-55e7-4cd5-8aa9-c4158c3c34ec#issue-4f3d9fb2-6cd5-4562-bb4a-4de1ece88743
    return f"{SNYK_ISSUES_URL_BASE}/{org_slug}/project/{project_id}#issue-{issue['key']}"

if __name__ == "__main__":
    main()
