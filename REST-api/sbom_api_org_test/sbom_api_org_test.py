import json
import argparse
import requests
import time
from termcolor import colored

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Snyk API Examples")
    parser.add_argument(
        "--orgId", type=str, help="The Snyk Organisation Id", required=True
    )
    parser.add_argument(
        "--snykToken", type=str, help="Your Snyk API Token", required=True
    )
    parser.add_argument(
        "--sbomFile", type=str, help="Your SBOM file", required=True
    )
    parser.add_argument(
        "--sbomFormat", type=str, help="Your SBOM format", required=True
    )
    parser.add_argument(
        "--breakOnBuild", type=str, help="Do you want to exit with code (1), option put Y or N", required=False
    )

    return parser.parse_args()

args = parse_command_line_args()
org_id = args.orgId
snyk_token = args.snykToken
sbom_file = args.sbomFile
sbom_format = args.sbomFormat
break_on_build = args.breakOnBuild


# Open the text file in read mode
with open(sbom_file, 'r') as file:
    text_data = file.read()

# Create the payload with the text data in the sbom element
payload = {
    "data": {
        "attributes": {
            "format": sbom_format,
            "sbom": json.loads(text_data)  # Load the JSON content from the file
        },
        "type": "resource"
    }
}

url = f"https://api.snyk.io/rest/orgs/{org_id}/sbom_tests"
params = {'version': '2023-10-13~beta'}
headers = {
    'Authorization': f'token {snyk_token}',
    'Content-Type': 'application/vnd.api+json',
    'accept': 'application/vnd.api+json'
}

response = requests.post(url, headers=headers, params=params, data=json.dumps(payload))

if response.status_code > 201:
    print(f"Error: {response.status_code} - {response.text}")
else:
    try:
        response_json = response.json()
        print(colored(json.dumps(response_json, indent=2), 'blue'))

        # Extract the "related" attribute
        related_url =f"https://api.snyk.io"+response_json.get("links", {}).get("related")

        if related_url:
            print(f"Related URL: {related_url}")
            # Check the scan status using the related URL
            while True:
                status_response = requests.get(related_url, headers=headers)
                if status_response.status_code == 200:
                    status_json = status_response.json()
                    # Check if the scan is finished
                    attribs = status_json.get("data", {}).get("attributes", {})
                    status = attribs.get("status")
                    if status is None or status == "finished":
                        print("Scan finished.")
                        print(colored(json.dumps(status_json, indent=2), 'green'))

                        if break_on_build == "Y":
                            vulns = attribs.get("test_summary",{}).get("vulnerabilities_by_severity")
                            critical = vulns.get("critical")
                            high = vulns.get("high")
                            if(critical>0 or high>0):
                                print("Critical or High Vulnerabilities found")
                                exit(1)

                        break
                    else:
                        print("Scan not finished yet. Waiting...")
                        time.sleep(1)  # Wait for 1 seconds before checking again
                else:
                    print(f"Error checking status: {status_response.status_code} - {status_response.text}")
                    break
        else:
            print("No related URL found in the response.")
    except json.JSONDecodeError:
        print("Error: Response is not in JSON format")