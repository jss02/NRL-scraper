"""
Module providing the "get_year" function that scrapes all matches in the given year.
"""

from round_scraper import get_round
from scraper import scrape_url
import sys

def get_year(year, to_json):
    """Retrieves match data for all games in the given year"""
    url = f"https://www.nrl.com/draw/?competition=111&round=1&season={year}"

    q_data_json = scrape_url(url, 'draw')
    
    rounds = q_data_json['filterRounds']
    
    for round in rounds:
       get_round(year, round['value'], to_json)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        get_year(sys.argv[1], sys.argv[2]=='json')
    elif len(sys.argv) == 4:
        for year in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
            get_year(year, sys.argv[3]=='json')
    else:
        print("Error! Usage: python3 src/year_scraper.py [year] [save type]")
        print("or")
        print("Error! Usage: python3 src/year_scraper.py [start year] [end year] [save type]")
        sys.exit(1)
        