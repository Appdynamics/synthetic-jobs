import requests

# Get the auth token using Synthetics Credential Vault
client_id = "<%CharlesLin-API-User%>" 
client_secret = "<%CharlesLin-API-Secret%>" 
token_url = 'http://se-demo-aws.demo.appdynamics.com:8090/controller/api/oauth/access_token'
payload={'grant_type': 'client_credentials', 'client_id':client_id, 'client_secret':client_secret}
response = requests.post(token_url, auth=(client_id, client_secret), data=payload)
print(response.json()['expires_in'])

# Send request API and validate returned objects
auth_header = {'Authorization': 'Bearer '+ response.json()['access_token']}
url="http://se-demo-aws.demo.appdynamics.com:8090/controller/rest/applications?output=JSON"
response=requests.get(url, headers=auth_header)
print(response.json())
assert len(response.json()) > 100