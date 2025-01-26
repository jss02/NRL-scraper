import psycopg2
from psycopg2 import sql
from psql_config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


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

def save_to_db(match_data, player_stat_metadata):
    connection = db_conn()
    if connection:
        cursor = connection.cursor()
    pass


# Test db connection
if __name__ == "__main__":
    save_to_db(1,2)