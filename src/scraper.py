"""
Module providing the 'scrape_url' function that scrapes match or draw data from nrl.com.
"""

import requests
from bs4 import BeautifulSoup
import html
import json

def scrape_url(url, type):
    """
    Scrapes match or draw data from the nrl.com website.

    Args:
        url (str): URL for the match/draw
            - URL for match is in the format "https://www.nrl.com/draw/{competition}/{year}/{round}/{match name}".
            - URL for draw is in the format "https://www.nrl.com/draw/?competition=111&round={round}&season={year}"

        type (str): Determines whether match data or draw data is scraped
            - 'match' for match data
            - 'draw' for draw data
    
    Returns:
        dict: JSON object containing match/draw data
    
    """

    # Determine whether draw data or match data is scraped
    element_id = 'vue-match-centre'
    if type == 'draw':
        element_id = "vue-draw"
        
    headers = {
        "User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find HTML element containing data
    data_element = soup.find(id=element_id)

    # The data is given as a HTML-escaped JSON string in the 'q-data' attribute
    q_data = html.unescape(data_element["q-data"])

    # Load data as JSON object
    data_json = json.loads(q_data)

    return data_json