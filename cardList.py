from cardsConfig import ID_BOARD
from credenciais import APIKey, APIToken
import requests
import json

def getCards():
    shortLinks = []
    for card in data: 
        shortLinks.append(card['shortLink'])
    return shortLinks

url = f"https://api.trello.com/1/boards/{ID_BOARD}/cards"

query = {
  'key': APIKey,
  'token': APIToken
}

response = requests.request(
   "GET",
   url,
   params=query
)

data = json.loads(response.text)
card_ids = []

for card in data:
  if card["id"] != "65d7876d72802fade3c98ebd":
      card_ids.append(card["id"])
#print(card_ids)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))