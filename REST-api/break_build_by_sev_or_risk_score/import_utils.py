# import_utils.py
import requests
import time

SNYK_API_URL = "https://snyk.io/api/v1"


def call_import_api(org_id, integration_id, snyk_token, github_repo, branch_name):
    url = f"{SNYK_API_URL}/org/{org_id}/integrations/{integration_id}/import"
    headers = {
        "Authorization": f"token {snyk_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "target": {
            "owner": github_repo.split('/')[0],
            "name": github_repo.split('/')[1],
            "branch": branch_name
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    location_header = response.headers.get("Location")
    if not location_header:
        raise Exception("Location header not found in response")

    return location_header

def poll_import_status(import_status_url, snyk_token):
    headers = {
        "Authorization": f"token {snyk_token}"
    }
    while True:
        response = requests.get(import_status_url, headers=headers)
        response.raise_for_status()
        status = response.json()["status"]
        if status == "complete":
            return response.json()["logs"][0]['projects']
        elif status == "failed":
            raise Exception("Import failed")
        time.sleep(1)

def get_projects(args):

    #first trigger the new import
    status_url = call_import_api(args.orgId, args.snykIntId, args.snykToken, args.scmRepo, args.scmRepoBranch)

    #now we have to wait until the inmport job is finsihed
    projects = poll_import_status(status_url, args.snykToken)

    return projects
