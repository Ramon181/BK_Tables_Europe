import mysql.connector
from dotenv import load_dotenv
from models.teams import teams
from models.league import leagues
from models.positions import positions
from os import environ

load_dotenv()


def db():
    data = mysql.connector.connect(
        host=environ.get("DB_HOST"),
        user=environ.get("DB_USER"),
        password=environ.get("DB_PASS"),
        database=environ.get("DB_NAME"),
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
