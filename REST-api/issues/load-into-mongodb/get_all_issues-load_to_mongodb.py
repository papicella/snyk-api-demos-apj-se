import requests
from pymongo import MongoClient
import argparse


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Snyk API Examples")
    parser.add_argument(
        "--orgId", type=str, help="The Snyk Organisation Id", required=True
    )
    parser.add_argument(
        "--apiToken", type=str, help="The Snyk API Token", required=True
    )
    parser.add_argument(
        "--mongodbPassword", type=str, help="The MongoDB Password", required=True
    )

    return parser.parse_args()

def get_snyk_issues(org_id, api_token):
    base_url = f"https://api.au.snyk.io/rest/orgs/{org_id}/issues"
    au_base_url = "https://api.au.snyk.io"

    headers = {
        "Authorization": f"token {api_token}",
        "Accept": "application/vnd.api+json"
    }
    params = {"limit": 100,
              "version": "2024-10-15",
              "type": "package_vulnerability"}

    all_issues = []
    next_url = base_url

    while next_url:
        response = requests.get(next_url, headers=headers, params=params if next_url == base_url else None)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break

        data = response.json()
        all_issues.extend(data.get("data", []))
        if "links" in data and "next" in data["links"]:
            next_url = data["links"]["next"]
            next_url = au_base_url + next_url;
            print("Fetching next set ..")
        else:
            next_url = None

    return all_issues

def insert_into_mongodb(issues, mongodb_connect_string, db_name, collection_name):

    client = MongoClient(mongodb_connect_string)
    db = client[db_name]
    collection = db[collection_name]
    if issues:
        for issue in issues:
            collection.insert_one(issue)  # Insert each issue individually
        print(f"Inserted {len(issues)} issues into MongoDB.")
    else:
        print("No issues to insert.")

if __name__ == "__main__":
    args = parse_command_line_args()

    ORG_ID = args.orgId
    API_TOKEN = args.apiToken
    MONGO_DB_PASSWORD = args.mongodbPassword

    DB_NAME = "snyk"
    COLLECTION_NAME = "sca_issues_pas_apples_org"
    MONGO_CONNECTION_STRING = f"mongodb+srv://pasapicella:{MONGO_DB_PASSWORD}@pas-mongodb-cluster.ik3ak.mongodb.net/snyk";

    print(f"using MongoDB URL", MONGO_CONNECTION_STRING)
    issues = get_snyk_issues(ORG_ID, API_TOKEN)
    print(f"Total issues fetched: {len(issues)}")

    insert_into_mongodb(issues, MONGO_CONNECTION_STRING, DB_NAME, COLLECTION_NAME)