import psycopg2
from psycopg2 import sql
from psql_config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from db_queries import *
def db_conn():
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
    try:
        cursor.execute(create_matches_table)
        cursor.execute(create_players_table)
        cursor.execute(create_player_stats_metadata_table)
        cursor.connection.commit()
    except Exception as e:
        print(f"Error creating tables: {e}")
        cursor.connection.rollback()

def get_match_tuple(match_data):
    match_duple = (
        match_data['matchId'],
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
        match_data['homeData'],
        match_data['awayData'],
        {'teamStats': match_data['teamStats']},
        match_data['playerStats']
        )

def save_to_db(match_data, player_stat_metadata):
    connection = db_conn()
    if connection:
        cursor = connection.cursor()
        create_tables(cursor)
        
        cursor.execute(insert_match_query, get_match_tuple(match_data))
        #cursor.execute(insert_players_query)

# Test db connection
if __name__ == "__main__":
    save_to_db(1,2)