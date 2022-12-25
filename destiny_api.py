from requests_oauthlib import OAuth2Session
from datetime import datetime
from dotenv import load_dotenv
import json
import os

load_dotenv()

api_key = os.getenv('API_KEY')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

redirect_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" 
auth_url = "https://www.bungie.net/en/OAuth/Authorize"
token_url = "https://www.bungie.net/platform/app/oauth/token/"
xur_url = "https://www.bungie.net/Platform/Destiny2/Vendors/?components=400,402"

session = OAuth2Session(client_id=client_id, redirect_uri=redirect_url)

auth_link = session.authorization_url(auth_url)
print(f"Authorization link: {auth_link[0]}")

redirect_response = input(f"Paste redirect link here: ")

session.fetch_token(
    client_id=client_id,
    client_secret=client_secret,
    token_url=token_url,
    authorization_response=redirect_response
)
header = { 
    'X-API-Key': api_key 
}

response = session.get(url=xur_url, headers=header)

data = json.loads(response.text)
###item = data['Response']['sales']['data']['2190858386']['saleItems']['0']
###print(f"{item['itemHash']}")

if(data['Response']['vendors']['data']['2190858386']['enabled']):
    print("Xur is available today")
else:
    print("Xur will be available at {['Response']['vendor']['data']['2190858386']['nextRefreshData']")

for items in data['Response']['sales']['data']['2190858386']['saleItems']:
    print(f"{data['Response']['sales']['data']['2190858386']['saleItems'][items]['itemHash']}")


# Print response
"""""
print("\n\n\n\n")
print(f"Response Status: {response.status_code}")
print(f"Response Reason: {response.reason}")
print(f"Data: \n{data}")

"""""


#Xur location and inventory
