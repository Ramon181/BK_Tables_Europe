import mysql.connector
from os import environ
from dotenv import load_dotenv
from models.teams import teams
from models.league import leagues
from models.positions import positions

load_dotenv()

def db():
    data = mysql.connector.connect(
        host=environ.get("DB_HOST", "localhost"),
        user=environ.get("DB_USER", "root"),
        password=environ.get("DB_PASS", "12345"),
        database=environ.get("DB_NAME", "tablas_db"),
    )
    return data

def create_tables():
    conn = db()
    cur = conn.cursor()
    cur.execute(teams)
    cur.execute(leagues)
    cur.execute(positions)
    cur.close()
    conn.close()

