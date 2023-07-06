import mysql.connector
from models.teams import teams
from models.league import leagues
from models.positions import positions



def db():
    data = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="tablas_db",
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
