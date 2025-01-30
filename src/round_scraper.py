"""
Module providing the "get_round" function that scrapes all matches in the given round in the given year.
"""

import sys
import os
import json
from scraper import scrape_url
from matchdataparser import parse_match_data
from match_db import save_to_db

def get_round(year, round, to_json=True):
    """
    Saves parsed match data into PostgreSQL database or as JSON files for all
    matches in the given round of the given year.
    
    If outputs are chosen to be saved as JSON files, Matches are saved in the
    directory "/{year}/{round}/", relative to the current working directory.
    The JSON files are named as "{year}_{round}_{match name}".

    If outputs are saved to database, user must have PostgreSQL database configured beforehand.

    Args:
        year (str): Year of matches
        round (str): Round of matches
        to_json (bool): True if data should be saved as JSON files

    Returns:
        None
    
    Raises:
        KeyError: If there is a missing key in the match data parsing process.
                  Saves the error causing input as error.json file.
    """
    if to_json:
        # Create directory to save json files
        directory = f"matches/{year}/round {round}"
        os.makedirs(directory, exist_ok=True)

    url = f"https://www.nrl.com/draw/?competition=111&round={round}&season={year}"

    draws_json = scrape_url(url, 'draw')
    
    for match in draws_json['fixtures']:
        match_url = "https://www.nrl.com" + match['matchCentreUrl']
        match_name = match['matchCentreUrl'].split('/')[-2]

        # Scrape match if game is finished
        if match["matchMode"] == "Post":
            # Get match data JSON object and parse
            match_data_json = scrape_url(match_url, 'match')

            # Save input to error file if key exception occurs during parsing for debugging
            try:
                match_data, metadata = parse_match_data(match_data_json['match'])
            except KeyError as e:
                with open('error.json', 'w') as f:
                    json.dump(match_data_json['match'], f, indent=4)
                raise KeyError
            
            if to_json:
                # Write to test file as JSON file
                file_path = os.path.join(directory, f'{year}_{round}_{match_name}.json')
                with open(file_path, 'w') as f:
                    json.dump(match_data, f, indent=4)
            else:
                # Save to db
                save_to_db(match_data, metadata)
        
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Error! Usage: python3 src/round_scraper.py [year] [round] [save type]")
        sys.exit(1)
    
    get_round(sys.argv[1], sys.argv[2], sys.argv[3]=='json')
