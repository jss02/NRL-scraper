import requests
from bs4 import BeautifulSoup
import html
import json
from matchdataparser import parse_match_data

headers = {
    "User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"
}

response = requests.get("https://www.nrl.com/draw/nrl-premiership/2002/round-23/bulldogs-v-eels/"
, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')

data_element = soup.find(id="vue-match-centre")


q_data = html.unescape(data_element["q-data"])

parsed_data = json.loads(q_data)
match_data = parse_match_data(parsed_data['match'])

with open('testjson2.json', 'w') as f:
    json.dump(match_data, f, indent=4)