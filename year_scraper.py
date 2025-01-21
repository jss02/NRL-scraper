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
    get_year(sys.argv[1])