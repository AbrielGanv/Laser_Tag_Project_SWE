import os

import psycopg2
from dotenv import load_dotenv

from udp_files.udp_transmit import broadcast_equipment_code

load_dotenv()

# Define connection parameters
connection_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

def add_player(player_id, codename):
    
    #adds a player to PostrgreSQL and broadcasts their equipment ID 

    conn = None
    cursor = None

    try:
        #connects to PostrgreSQL
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        #adds player to database
        cursor.execute('''
            INSERT INTO players (id, codename)
            VALUES (%s, %s);
            ''', (player_id, codename))

        #saves the database change
        conn.commit()

        print(f"Added player {codename} with equipment ID {player_id}")

        #broadcasts after the DB commits
        broadcast_equipment_code(player_id)

    except Exception as error:
        if conn:
            conn.rollback()
        print(f"Error adding player: {error}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    add_player(504, "TestPlayer5")