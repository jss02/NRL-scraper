"""
Module providing the "get_round" function that scrapes all matches in the given round in the year
"""

import sys
import os
import json
from scraper import scrape_url
from matchdataparser import parse_match_data

def get_round(year, round):
    # Create directory to save json files
    directory = f"{year}/{round}"
    os.makedirs(directory, exist_ok=True)

    url = f"https://www.nrl.com/draw/?competition=111&round={round}&season={year}"

    draws_json = scrape_url(url, 'draw')

    with open("testround.json", "w") as f:
        json.dump(draws_json['fixtures'], f, indent=4)
    
    for match in draws_json['fixtures']:
        match_url = "https://www.nrl.com" + match['matchCentreUrl']
        match_name = match['matchCentreUrl'].split('/')[-2]

        # Scrape match if game is finished
        if match["matchMode"] == "Post":
            # Get match data JSON object and parse
            match_data_json = scrape_url(match_url, 'match')
            match_data = parse_match_data(match_data_json['match'])
        
            # Write to test file as JSON file
            file_path = os.path.join(directory, f'{year}_{round}_{match_name}.json')
            with open(file_path, 'w') as f:
                json.dump(match_data, f, indent=4)
        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error! Usage: python3 get_round.py [year] [round]")
        sys.exit(1)
    
    get_round(sys.argv[1], sys.argv[2])
