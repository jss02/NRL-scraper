"""
File containing the database schemas as strings.
"""

create_matches_table = """
CREATE TABLE IF NOT EXISTS matches (
    matchId INTEGER PRIMARY KEY,
    gameSeconds INTEGER NOT NULL,
    roundNumber INTEGER NOT NULL,
    startTime TIMESTAMPZ NOT NULL,
    url TEXT NOT NULL,
    venue VARCHAR(100) NOT NULL,
    attendance INTEGER,
    groundConditions VARCHAR(50),
    weather VARCHAR(50),
    homeTeamId INTEGER NOT NULL,
    awayTeamId INTEGER NOT NULL,
    homeScore INTEGER NOT NULL,
    awayScore INTEGER NOT NULL,
    homeData JSONB NOT NULL,
    awayData JSONB NOT NULL,
    teamStats JSONB NOT NULL,
    playerStats JSONB NOT NULL 
);
"""

create_players_table = """
CREATE TABLE IF NOT EXISTS players (
playerId INTEGER PRIMARY KEY,
firstName VARCHAR(50) NOT NULL,
lastName VARCHAR(50) NOT NULL
);
"""

create_player_stats_metadata_table = """
CREATE TABLE IF NOT EXISTS player_stats_metadata (
    name VARCHAR(50) PRIMARY KEY,
    type VARCHAR(20) NOT NULL,
    units VARCHAR(20) NOT NULL
);
"""

