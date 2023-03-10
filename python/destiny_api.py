from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import json
import os

#load the client id, secret, and api key from the .env file
load_dotenv()
api_key = os.getenv('API_KEY')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

redirect_url = "https://www.google.com"    
auth_url = "https://www.bungie.net/en/OAuth/Authorize"
token_url = "https://www.bungie.net/platform/app/oauth/token/"

session = OAuth2Session(client_id=client_id, redirect_uri=redirect_url) #session used to authenticate, 
auth_link = session.authorization_url(auth_url)
print(f"{auth_link[0]}")
redirect_response = input(f"Paste redirect link here: ")

#parses the redirect url for code and uses it to obtain access and refresh token
token = session.fetch_token(
    client_id=client_id,
    client_secret=client_secret,
    token_url=token_url,
    authorization_response=redirect_response
)
header = { 
    'X-API-Key': api_key 
}

#use GetLinkedProfile endpoint to get user membership type and id
profile_url = "https://www.bungie.net/Platform/Destiny2/-1/Profile/" + f"{token['membership_id']}" + "/LinkedProfiles/"
response = session.get(url=profile_url, headers=header)
data = json.loads(response.text)

membership_id = data['Response']['profiles'][0]['membershipId']
membership_type = data['Response']['profiles'][0]['membershipType']

#Use GetCharacter endpoint to get character id of the character of users choosing
character_url = f"https://www.bungie.net/Platform/Destiny2/{membership_type}/Profile/{membership_id}/?components=200"
response = session.get(url=character_url, headers=header)
data = json.loads(response.text)
which_character = input("Which character would you like to view Xur's inventory on?: ")
for characters in data['Response']['characters']['data']:
    if data['Response']['characters']['data'][characters]['classHash']==671679327 and which_character=='hunter':
        character_id = characters
    if data['Response']['characters']['data'][characters]['classHash']==2271682572 and which_character=='warlock':
        character_id = characters
    if data['Response']['characters']['data'][characters]['classHash']==3655393761 and which_character=='titan':
        character_id = characters

#xur and Destiny Manifest endpoint
xur_url = f"https://www.bungie.net/Platform/Destiny2/{membership_type}/Profile/{membership_id}/Character/{character_id}/Vendors/2190858386/?components=304,305,402"
manifest_url = "https://www.bungie.net/Platform/Destiny2/Manifest/DestinyInventoryItemDefinition/"

response = session.get(url=xur_url, headers=header)
xur_data = json.loads(response.text)

print("ITEMS SOLD")
for item in xur_data['Response']['sales']['data']:  #iterate through the items that xur is selling and 
    if item != '0' and item != '567':
        item_hash = xur_data['Response']['sales']['data'][item]['itemHash']

        response = session.get(url=f'{manifest_url}{item_hash}/', headers=header)
        item_data = json.loads(response.text)

        item_name = item_data['Response']['displayProperties']['name']
        print(f'{item_name}, ', end="")

            




