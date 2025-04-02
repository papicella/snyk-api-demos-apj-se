# set_ignores

Python script to set ignore rules on issues for Snyk projects.

## Prerequisites

- Python 3.x
- Install required packages: `pip install -r requirements.txt`

## Usage

```sh
usage: set_ignores.py --orgId ORGID --snykToken SNYKTOKEN [--projId PROJID]

Arguments
--orgId ORGID: The organization ID in Snyk.
--snykToken SNYKTOKEN: The Snyk API token.
--projId PROJID (optional): The project ID in Snyk.