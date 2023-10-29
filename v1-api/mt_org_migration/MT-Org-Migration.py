import http.client
import json
import os
import sys
import time

MT = os.environ.get('MT') or sys.exit("Please check env var: MT") #MT ENV
SNYK_TOKEN_US = os.environ.get('SNYK_TOKEN_US') or sys.exit("Please check env var: SNYK_TOKEN_US") #US API KEY
SNYK_TOKEN_MT = os.environ.get('SNYK_TOKEN_MT') or sys.exit("Please check env var: SNYK_TOKEN_MT") #MT API KEY
GROUP_ID_US = os.environ.get('GROUP_ID_US') or sys.exit("Please check env var: GROUP_ID_US") #Group ID of US Group to clone from
GROUP_ID_MT = os.environ.get('GROUP_ID_MT') or sys.exit("Please check env var: GROUP_ID_MT") #Group ID of MT Group to clone to
SOURCE_ORG_ID = os.environ.get('SOURCE_ORG_ID') #Optional - Org ID of MT Org to copy settings from
PAGE_NO = os.environ.get('PAGE') or 1 #Optional - page number if there is > 100 orgs
DELAY = os.environ.get('DELAY') or 1 #Optional - to avoid rate limiting

connectionUS = http.client.HTTPSConnection('api.snyk.io')
connectionMT = http.client.HTTPSConnection('app.{}.snyk.io'.format(MT.lower())) if (MT.lower() == 'au') or (MT.lower() == 'eu') else sys.exit("Please check env var: MT - must be either AU or EU")

headersUS = {
  'Content-Type': 'application/json',
  'Authorization': 'token {}'.format(SNYK_TOKEN_US)
}

headersMT = {
  'Content-Type': 'application/json',
  'Authorization': 'token {}'.format(SNYK_TOKEN_MT)
}

# get set of orgs
orgsResponse = connectionUS.request('GET', '/api/v1/group/{}/orgs?perPage=100&page={}'.format(GROUP_ID_US, PAGE_NO), '', headersUS)
orgsResponseStatus = connectionUS.getresponse()
orgsResponse = json.loads(orgsResponseStatus.read())

if len(orgsResponse['orgs']) > 0 and orgsResponseStatus.status == 200:
  print("\nCloning {} orgs from {} group".format(len(orgsResponse['orgs']),orgsResponse['name']))
  for org in orgsResponse['orgs']:
    #for each org, get list of issues
    print("Cloning org: {} to MT Instance".format(org['name']))

    body = {
      "name": org['name'],
      "groupId": "{}".format(GROUP_ID_MT), #add the right group id - Add MT Group Id
      "sourceOrgId": "{}".format(SOURCE_ORG_ID if SOURCE_ORG_ID is not None else "") #This is the source org id.
    }
    print(body)
    createOrgs = connectionMT.request('POST', '/api/v1/org', json.dumps(body), headersMT)
    createOrgsStatus = connectionMT.getresponse()
    createOrgs =  json.loads(createOrgsStatus.read())

    print("{} {} - {}".format(createOrgsStatus.status, createOrgsStatus.reason, createOrgs['message']))

    time.sleep(DELAY)
else:
    print("{} {} - {}".format(orgsResponseStatus.status, orgsResponseStatus.reason))