def get_team_data(team_json):
    team_keys = ['teamId', 'nickName', 'name', 'score']
    team_data = {key: team_json.get(key, None) for key in team_keys}

    # Copy scoring data
    team_scoring_json = team_json['scoring']
    team_data['conversionsAttempts'] = team_scoring_json['conversions']['attempts']
    team_data['conversionsMade'] = team_scoring_json['conversions']['made']
    team_data['tries'] = team_scoring_json['tries']['made']
    team_data['halfTimeScore'] = team_scoring_json['halfTimeScore']

    return team_data

def get_team_stats(team_stats_json):
    team_stats = {}
    for stat_group in team_stats_json:
        for stat in stat_group['stats']:
            stat_title = stat['title']
            if stat_title == 'Used':
                stat_title = 'Interchanges'
            team_stats[stat_title] = {
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
                team_stats[stat_title]['home']['numerator'] = stat['homeValue']['numerator']
                team_stats[stat_title]['home']['denominator'] = stat['homeValue']['denominator']
                team_stats[stat_title]['away']['numerator'] = stat['awayValue']['numerator']
                team_stats[stat_title]['away']['denominator'] = stat['awayValue']['denominator']

    return team_stats

def get_player_stats(player_stats_json):
    # List of players and their stats
    home_players = player_stats_json['homeTeam']
    


def parse_match_data(match_data_json):
    # Copy relevant game info
    match_keys = ['matchId', 'matchMode', 'matchState', 'gameSeconds', 'roundNumber', 'roundTitle', 'startTime', 'url','venue', 'venueCity', 'attendance', 'groundConditions', 'hasExtraTime', 'weather'] 

    match_data = {key: match_data_json.get(key, None) for key in match_keys}

    # Copy relevant home team data
    match_data['homeData'] = get_team_data(match_data_json['homeTeam'])

    # Copy away team data
    match_data['awayData'] = get_team_data(match_data_json['awayTeam'])

    team_stats_json = match_data_json['stats']['groups']
    team_stats = get_team_stats(team_stats_json)
    match_data['teamStats'] = team_stats

    match_data['playerStats'] = match_data_json['stats']['players']
    

    return match_data