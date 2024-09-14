# list_issues_with_fixedIn_version

Python script to create CSV file with issues together with FixedIn version.

[2022/12/23] Modification:
- Skip if `issueType` is not "vuln"
- Added `Priority score` column

## Prerequisite

- Python
- `pip install pysnyk`
  - https://pypi.org/project/pysnyk/

## Usage

```
python3 list_issues_with_fixedIn_version.py --orgId <Org Id> --projectId <Project ID>
```