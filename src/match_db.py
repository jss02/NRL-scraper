"""
Module providing the "save_to_db" function for saving match data to PostgreSQL database.
Must have PostgreSQL database configured beforehand.
"""

import psycopg2
from psql_config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from db_queries import *
import json

def db_conn():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None

def create_tables(cursor):
    """Create tables in the database"""
    try:
        cursor.execute(create_matches_table)
        cursor.execute(create_players_table)
        cursor.execute(create_player_stats_metadata_table)
        cursor.connection.commit()
    except Exception as e:
        print(f"Error creating tables: {e}")
        cursor.connection.rollback()

def get_match_tuple(match_data):
    """Create tuple containing match data"""
    match_tuple = (
        int(match_data['matchId']),
        match_data['gameSeconds'],
        match_data['roundNumber'],
        match_data['startTime'],
        match_data['url'],
        match_data['venue'],
        match_data['attendance'],
        match_data['groundConditions'],
        match_data['weather'],
        match_data['homeData']['teamId'],
        match_data['awayData']['teamId'],
        match_data['homeData']['score'],
        match_data['awayData']['score'],
        json.dumps(match_data['homeData']),
        json.dumps(match_data['awayData']),
        json.dumps({'teamStats': match_data['teamStats']}),
        json.dumps(match_data['playerStats'])
        )

    return match_tuple

def insert_players(cursor, players_json):
    """Insert player data into players table"""
    for key in players_json:
        for player in players_json[key]:
            cursor.execute(insert_player_query, (player['playerId'], player['firstName'], player['lastName']))
    cursor.connection.commit()

def insert_player_stats_metadata(cursor, metadata):
    """Insert player stats metadata into player_stats_metadata table"""
    for group in metadata:
        for stat in group['stats']:
            cursor.execute(insert_player_stats_metadata_query, (stat['name'], stat['type']))
    cursor.connection.commit()

def save_to_db(match_data, player_stats_metadata, overwrite=False):
    """Save match data into database"""
    connection = db_conn()
    if connection:
        cursor = connection.cursor()
        create_tables(cursor)
        
        try:
            cursor.execute(insert_match_query, get_match_tuple(match_data))
            cursor.connection.commit()
        except psycopg2.errors.UniqueViolation as e:
            print("Error: match already exists in db")
            cursor.connection.rollback()

        insert_players(cursor, match_data['players'])
        insert_player_stats_metadata(cursor, player_stats_metadata)