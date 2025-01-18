"""
Module providing the 'scrape_url' function that scrapes match data from NRL.com matches.
"""

import requests
from bs4 import BeautifulSoup
import html
import json

def scrape_url(url):
    """
    Scrapes match data from the NRL.com website

    Args:
        url (str): URL for the match in the format "nrl.com/draw/{competition}/{year}/{round}/{match name}".
    
    Returns:
        dict: JSON object containing match data
    
    """

    headers = {
        "User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find HTML element containing match data
    data_element = soup.find(id="vue-match-centre")

    # The data is given as a HTML-escaped JSON string in the 'q-data' attribute
    q_data = html.unescape(data_element["q-data"])

    # Load data as JSON object
    data_json = json.loads(q_data)

    return data_json