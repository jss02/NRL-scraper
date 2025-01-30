"""
Module containing the database schemas as strings.
"""

create_matches_table = """
CREATE TABLE IF NOT EXISTS matches (
    match_id BIGINT PRIMARY KEY,
    game_seconds INTEGER NOT NULL,
    round_number INTEGER NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    url TEXT NOT NULL,
    venue VARCHAR(100) NOT NULL,
    attendance INTEGER,
    ground_conditions VARCHAR(50),
    weather VARCHAR(50),
    home_team_id INTEGER NOT NULL,
    away_team_id INTEGER NOT NULL,
    home_score INTEGER NOT NULL,
    away_score INTEGER NOT NULL,
    home_data JSONB NOT NULL,
    away_data JSONB NOT NULL,
    team_stats JSONB NOT NULL,
    player_stats JSONB NOT NULL 
);
"""

create_players_table = """
CREATE TABLE IF NOT EXISTS players (
    player_id BIGINT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);
"""

create_player_stats_metadata_table = """
CREATE TABLE IF NOT EXISTS player_stats_metadata (
    name VARCHAR(50) PRIMARY KEY,
    type VARCHAR(20) NOT NULL
);
"""

insert_match_query = """
INSERT INTO matches (
    match_id, game_seconds, round_number, start_time, url, venue,
    attendance, ground_conditions, weather, home_team_id, away_team_id,
    home_score, away_score, home_data, away_data, team_stats, player_stats
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

insert_player_query = """
INSERT INTO players (
    player_id, first_name, last_name
)
VALUES (%s, %s, %s)
ON CONFLICT (player_id) DO NOTHING;
"""

insert_player_stats_metadata_query = """
INSERT INTO player_stats_metadata (
    name, type
)
VALUES (%s, %s)
ON CONFLICT (name) DO NOTHING;
"""