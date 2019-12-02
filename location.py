import requests
import json

url = 'https://extreme-ip-lookup.com/json/'
r = requests.get(url)
data = json.loads(r.content.decode())
print(data)

print(data["lon"])
print(data["lat"])

print(25 if 1 < 2 else 30)