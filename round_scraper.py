"""
Module providing the "get_round" function that scrapes all matches in the given round in the year
"""

import requests
from bs4 import BeautifulSoup
import sys
import html
import json
from scraper import scrape_url
from matchdataparser import parse_match_data

def get_round(year, round):
    url = f"https://www.nrl.com/draw/?competition=111&round={round}&season={year}"

    headers = {
        "User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    draws_element = soup.find(id="vue-draw")

    # The draws are given in a HTML-escaped JSON string in the 'q-data' attribute
    q_data = html.unescape(draws_element["q-data"])
    # Load data as JSON object
    draws_json = json.loads(q_data)

    with open("testround.json", "w") as f:
        json.dump(draws_json['fixtures'], f, indent=4)
    
    for match in draws_json['fixtures']:
        match_url = "https://www.nrl.com" + match['matchCentreUrl']
        match_name = match['matchCentreUrl'].split('/')[-2]

        # Scrape match if game is finished
        if match["matchMode"] == "Post":
            # Get match data JSON object and parse
            match_data_json = scrape_url(match_url)
            match_data = parse_match_data(match_data_json['match'])
        
            # Write to test file as JSON file
            with open(f'{year}_{round}_{match_name}.json', 'w') as f:
                json.dump(match_data, f, indent=4)
        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error! Usage: python3 get_round.py [year] [round]")
        sys.exit(1)
    
    get_round(sys.argv[1], sys.argv[2])
