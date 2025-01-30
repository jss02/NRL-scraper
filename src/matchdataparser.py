"""
Module providing 'parse_match_data' function for parsing useful match data and
statistics.

The 'parse_match_data' function filters out unhelpful values such as images,
team themes, metadata, and other irrelevant data in the JSON object obtained by
scraping NRL.com matches. 
"""


def get_team_data(team_json):
    """Extract useful team data from the JSON object containing team info"""

    team_keys = ['teamId', 'name', 'nickName', 'score']
    team_data = {key: team_json[key] for key in team_keys}

    # Copy scoring data. If key not present then default to 0.
    team_data['conversionsAttempts'] = 0
    team_data['conversionsMade'] = 0
    team_data['tries'] = 0

    # Populate with values from JSON object if they exist
    team_scoring_json = team_json['scoring']
    team_data['halfTimeScore'] = team_scoring_json['halfTimeScore']
    if 'conversions' in team_scoring_json:
        team_data['conversionsAttempts'] = team_scoring_json['conversions']['attempts']
        team_data['conversionsMade'] = team_scoring_json['conversions']['made']
    
    if 'tries' in team_scoring_json:
        team_data['tries'] = team_scoring_json['tries']['made']

    return team_data

def get_team_stats(team_stats_json):
    """Get list containing useful team stats from JSON object containing team stats"""

    team_stats_list = []
    for stat_group in team_stats_json:
        for stat in stat_group['stats']:
            stat_title = stat['title']

            # Stat with title 'used' is the number of interchanges used
            if stat_title == 'Used':
                stat_title = 'Interchanges'

            team_stats = {
                'title': stat_title,
                'type': stat['type'],
                'home': {
                    'value':  stat['homeValue']['value'],
                },
                'away': {
                    'value': stat['awayValue']['value'],
                },
            }

            # Copy numerator and denominator values if they exist
            if 'numerator' in stat['homeValue']:
                team_stats['home']['numerator'] = stat['homeValue']['numerator']
                team_stats['home']['denominator'] = stat['homeValue']['denominator']
                team_stats['away']['numerator'] = stat['awayValue']['numerator']
                team_stats['away']['denominator'] = stat['awayValue']['denominator']
            
            team_stats_list.append(team_stats)

    return team_stats_list

def parse_players(players_json):
    """Deletes player images from player details JSON objects"""
    for player_json in players_json:
        player_json.pop('headImage', None)
        player_json.pop('bodyImage', None)
        player_json.pop('url', None)

    return

def parse_match_data(match_data_json):
    """
    Filter unhelpful data from the match data JSON object obtained by scraping NRL.com matches.

    Args:
        match_data_json (dict): JSON object of match data to extract from.

    Returns:
        dict: JSON object of useful data.

    Raises:
        KeyError: If a key is missing from the JSON object.
    """

    # Copy useful game info
    match_keys = ['matchId', 'matchMode', 'matchState', 'gameSeconds', 'roundNumber', 'roundTitle', 'startTime', 'url','venue', 'venueCity', 'attendance', 'groundConditions', 'hasExtraTime', 'weather'] 

    match_data = {key: match_data_json.get(key, None) for key in match_keys}

    # Copy home team data
    match_data['homeData'] = get_team_data(match_data_json['homeTeam'])

    # Copy away team data
    match_data['awayData'] = get_team_data(match_data_json['awayTeam'])

    # Get list of players
    home_players = match_data_json['homeTeam']['players']
    away_players = match_data_json['awayTeam']['players']
    parse_players(home_players)
    parse_players(away_players)
    match_data['players'] = {'home': home_players, 
                             'away': away_players}

    # Get team stats and save to match_data object
    team_stats_json = match_data_json['stats']['groups']
    team_stats = get_team_stats(team_stats_json)
    match_data['teamStats'] = team_stats

    # Save player stats
    match_data['playerStats'] = match_data_json['stats']['players']

    # Separate metadata for player stats
    player_stats_metadata = match_data['playerStats']['meta']
    del match_data['playerStats']['meta']

    return match_data, player_stats_metadata