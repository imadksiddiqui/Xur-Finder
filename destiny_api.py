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

### user_details_endpoint = "https://www.bungie.net/Platform/User/GetCurrentBungieNetUser/"
### response = session.get(url=user_details_endpoint, headers = header)
response = session.get(url=xur_url, headers=header)

data = json.loads(response.text)
###item = data['Response']['sales']['data']['2190858386']['saleItems']['0']
###print(f"{item['itemHash']}")

xur = data['Response']['sales']['data']['2190858386']['saleItems']['1']
###for itemHash in xur:
 ###       print(f" {itemHash['costs']}")


# Print response
"""""
print("\n\n\n\n")
print(f"Response Status: {response.status_code}")
print(f"Response Reason: {response.reason}")
print(f"Data: \n{data}")

"""""


#Xur location and inventory

"""""
# Make the API request
response = requests.get(xur_url, headers=header)
print(f"Xur text: \n{response.text}" )


# Load the JSON data from the response
data = json.loads(response.text)

# Find Xur's vendor hash
for vendor in data['Response']['vendors']:
    if vendor['vendorName'] == "Xur":
        xur = vendor['vendorHash']

# Find Xur's location and items for sale
for vendor in data['Response']['vendors']:
    if vendor['vendorHash'] == xur:
        location = vendor['location']['activityHash']
        items_for_sale = vendor['saleItems']

# Print Xur's location and items for sale
print(f"Xur is located at activity {location}.")
print("\nItems for sale:")
for item in items_for_sale:
    print("\n"+item['item']['itemName'])
"""""