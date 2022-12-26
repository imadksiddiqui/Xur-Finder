from requests_oauthlib import OAuth2Session
from datetime import datetime
from dotenv import load_dotenv
import json
import os

load_dotenv()

api_key = os.getenv('API_KEY')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

redirect_url = "https://www.google.com"    
auth_url = "https://www.bungie.net/en/OAuth/Authorize"
token_url = "https://www.bungie.net/platform/app/oauth/token/"
user_url = "https://www.bungie.net/Platform/User/GetMembershipsForCurrentUser/"

session = OAuth2Session(client_id=client_id, redirect_uri=redirect_url)

auth_link = session.authorization_url(auth_url)
print(f"{auth_link[0]}")
redirect_response = input(f"Paste redirect link here: ")

token = session.fetch_token(
    client_id=client_id,
    client_secret=client_secret,
    token_url=token_url,
    authorization_response=redirect_response
)
header = { 
    'X-API-Key': api_key 
}
print(token)
#print(f"Access token: {token['access_token']} \n Refresh token: {token['refresh_token']}")
response = session.get(url=user_url, headers=header)
data = json.loads(response.text)

membership_id = data['Response']['destinyMemberships'][0]['membershipId']
membership_type = data['Response']['destinyMemberships'][0]['membershipType']


"""""
if(data['Response']['vendors']['data']['2190858386']['enabled']):
    print("Xur is available today")
else:
    print("Xur will be available at {['Response']['vendor']['data']['2190858386']['nextRefreshData']")

for items in data['Response']['sales']['data']['2190858386']['saleItems']:
    print(f"{data['Response']['sales']['data']['2190858386']['saleItems'][items]['itemHash']}")
"""""
