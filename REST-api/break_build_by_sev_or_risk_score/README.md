# break the build by servirty or risk score

Python script to retrieve the Ignores on issues for SCM targets or projects.

## Prerequisites

- Python 3.x
- Install required packages: `pip install -r requirements.txt`## Usage

```sh
usage: check-vulns.py --orgId ORGID --snykToken SNYKTOKEN --scmRepo SCMREPO --scmRepoBranch SCMREPOBRANCH --snykIntId SNYKINTID [--projId PROJID]

Arguments
--orgId ORGID: The organization ID in Snyk.
--snykToken SNYKTOKEN: The Snyk API token.
--scmRepo SCMREPO: The SCM repository in the format owner/repo.
--scmRepoBranch SCMREPOBRANCH: The branch name of the SCM repository.
--snykIntId SNYKINTID: The Snyk integration ID.
--projId PROJID (optional): The project ID in Snyk.
--riskScoreThreshold RISKSCORETHRESHOLD (optional): Break the build by risk score instead of severity on the given threshold.
```

## Description
This script performs the following steps:


Trigger Import: Calls the Snyk import API to trigger a new import for the specified SCM repository and branch.
Poll Import Status: Polls the import status until it is complete or fails.
Retrieve Issues: Retrieves the list of issues for the imported projects.
Check Vulnerabilities: Checks the vulnerabilities based on severity or risk score.

## Functions

call_import_api(org_id, integration_id, snyk_token, github_repo, branch_name)
Triggers the Snyk import API for the specified repository and branch.


poll_import_status(import_status_url, snyk_token)
Polls the import status until it is complete or fails.


get_projects(args)
Triggers the import and waits for it to complete, then retrieves the list of projects.


get_unified_issues(orgid, project_id, snyk_token, ignored)
Retrieves the list of issues for the specified project.


check_vulnerabilities(issues)
Checks the vulnerabilities based on severity or risk score.


License
This project is licensed under the MIT License.