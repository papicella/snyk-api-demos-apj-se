import argparse

from snyk import SnykClient
from utils import get_default_token_path, get_token

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Snyk API Examples")
    parser.add_argument(
        "--orgId", type=str, help="The Snyk Organisation Id", required=True
    )
    parser.add_argument(
        "--projectId", type=str, help="The project ID in Snyk", required=True
    )
    return parser.parse_args()

def listToString(s):
    str1 = ""
    if s:
        for ele in s:
            str1 += ele + " "
    return str1

snyk_token_path = get_default_token_path()
snyk_token = get_token(snyk_token_path)
args = parse_command_line_args()
org_id = args.orgId
project_id = args.projectId

client = SnykClient(snyk_token)
issue_set = client.organizations.get(org_id).projects.get(project_id).issueset_aggregated.all()

# CSV Header
print("Priority Score, Package Name, Package Versions, Title, Fixed In version")

for v in issue_set.issues:
    # print(v)  # debug

    # Skip if issueType is not "vuln"
    if v.issueType == "vuln":
        print('%s, %s, %s, %s, %s' %
          (
            v.priorityScore,
            v.pkgName,
            listToString(v.pkgVersions),
            v.issueData.title,
            listToString(v.fixInfo.fixedIn)
          )
        )