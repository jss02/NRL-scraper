"""

"""

from round_scraper import get_round
from scraper import scrape_url
import sys

def get_year(year):
    url = f"https://www.nrl.com/draw/?competition=111&round=1&season={year}"

    q_data_json = scrape_url(url, 'draw')
    
    rounds = q_data_json['filterRounds']
    
    for round in rounds:
       get_round(year, round['value'])

if __name__ == '__main__':
    if len(sys.argv) == 2:
        get_year(sys.argv[1])
    elif len(sys.argv) == 3:
        for year in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
            get_year(year)
    else:
        print("Error! Usage: python3 src/year_scraper.py [year]")
        print("or")
        print("Error! Usage: python3 src/year_scraper.py [start year] [end year]")
        sys.exit(1)
        