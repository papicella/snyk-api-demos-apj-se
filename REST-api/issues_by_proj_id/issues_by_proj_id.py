import requests
from urllib.parse import urlencode

SNYK_REST_API_URL = "https://api.snyk.io"

def get_unified_issues(orgid,project_id,snyk_token,ignored):
    url = f"{SNYK_REST_API_URL}/rest/orgs/{orgid}/issues"

    headers = {
        'Authorization': f'token {snyk_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.api+json'
    }

    params = {
        "ignored": ignored,
        "version": "2024-08-22",
        "status": "open",
        "limit": 100
    }

    if project_id:
        params["scan_item.type"] = "project"
        params["scan_item.id"] = project_id

    url = f"{url}?{urlencode(params)}"

    all_issues = []

    while url:
        response = requests.get(url,  headers=headers)
        data = response.json()
        all_issues.extend(data['data'])
        next = data['links'].get('next')
        if next is None:
            break
        url = SNYK_REST_API_URL + "/" + next

    return all_issues
