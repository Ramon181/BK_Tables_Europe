from flask import Flask
from flask_cors import CORS
from db import create_tables
from routes.routePositions import positions_bp
from routes.routeTeams import teams_bp
from routes.routeLeague import league_bp
app = Flask(__name__)
CORS(app)

app.register_blueprint(positions_bp)
app.register_blueprint(teams_bp)
app.register_blueprint(league_bp)

@app.route("/")
def index():
    return "hola mundo"

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)