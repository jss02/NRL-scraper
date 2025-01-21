from matchdataparser import parse_match_data
from scraper import scrape_url
import json

def main(url):
    # Get match data JSON object and parse
    match_data_json = scrape_url(url, 'match')
    match_data = parse_match_data(match_data_json['match'])

    # Write to test file as JSON file
    with open('output.json', 'w') as f:
        json.dump(match_data, f, indent=4)

if __name__ == '__main__':
    main("https://www.nrl.com/draw/nrl-premiership/2024/grand-final/storm-v-panthers/")