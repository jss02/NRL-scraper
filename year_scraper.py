"""

"""
import requests
from bs4 import BeautifulSoup
from round_scraper import get_round
import sys
import html
import json

def get_year(year):
    url = f"https://www.nrl.com/draw/?competition=111&round=1&season={year}"

    headers = {
        "User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    draws_element = soup.find(id="vue-draw")
    # The draws are given in a HTML-escaped JSON string in the 'q-data' attribute
    q_data = html.unescape(draws_element["q-data"])

    # Load data as JSON object
    q_data_json = json.loads(q_data)

    rounds = q_data_json['filterRounds']
    
    for round in rounds:
       get_round(year, round['value'])

if __name__ == '__main__':
    get_year(sys.argv[1])