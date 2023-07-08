from flask import Blueprint, jsonify, request
import json
from db import db

positions_bp = Blueprint("positions", __name__)


@positions_bp.get("/positions")
def get_positions():
    conn = db()
    cursor = conn.cursor()

    try:
        # Realizar una consulta JOIN para obtener las posiciones con las relaciones
        query = """
        SELECT p.id, l.league_name, t.team_name, t.position, t.matches_played, t.games_won,
               t.games_drawn, t.games_lost, t.goals_for, t.goals_against, t.points
        FROM positions p
        JOIN teams t ON p.team_id = t.id
        JOIN leagues l ON p.league_id = l.id
        """
        cursor.execute(query)
        positions = cursor.fetchall()

        # Crear la lista de objetos en el formato deseado
        leagues_dict = {}
        for position in positions:
            position_id = position[0]
            league_name = position[1]
            team_name = position[2]
            position_info = {
                "team_name": team_name,
                "position": position[3],
                "matches_played": position[4],
                "games_won": position[5],
                "games_drawn": position[6],
                "games_lost": position[7],
                "goals_for": position[8],
                "goals_against": position[9],
                "points": position[10],
            }
            if league_name not in leagues_dict:
                leagues_dict[league_name] = {
                    "id": position_id,
                    "league_name": league_name,
                    "teams": [position_info],
                }
            else:
                leagues_dict[league_name]["teams"].append(position_info)

        # Obtener la lista de ligas
        leagues = list(leagues_dict.values())

        # Devolver la lista de objetos en formato JSON
        return jsonify(leagues)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()


@positions_bp.post("/positions")
def post_positions():
    conn = db()
    cursor = conn.cursor()

    try:
        data = request.get_json()

        # Obtener el nombre de la liga del objeto JSON
        league_name = data.get("league_name")

        # Insertar la liga en la tabla "leagues"
        cursor.execute("INSERT INTO leagues (league_name) VALUES (%s)", (league_name,))
        league_id = cursor.lastrowid

        # Obtener la matriz de equipos del objeto JSON
        teams = data.get("teams")

        for team_data in teams:
            # Obtener los datos individuales del equipo
            team_name = team_data.get("team_name")
            position = team_data.get("position")
            matches_played = team_data.get("matches_played")
            games_won = team_data.get("games_won")
            games_drawn = team_data.get("games_drawn")
            games_lost = team_data.get("games_lost")
            goals_for = team_data.get("goals_for")
            goals_against = team_data.get("goals_against")
            points = team_data.get("points")

            # Insertar el equipo en la tabla "teams"
            cursor.execute(
                "INSERT INTO teams (team_name, position, matches_played, games_won, games_drawn, games_lost, goals_for, goals_against, points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    team_name,
                    position,
                    matches_played,
                    games_won,
                    games_drawn,
                    games_lost,
                    goals_for,
                    goals_against,
                    points,
                ),
            )
            team_id = cursor.lastrowid

            # Insertar la posición en la tabla "positions"
            cursor.execute(
                "INSERT INTO positions (team_id, league_id) VALUES (%s, %s)",
                (team_id, league_id),
            )

        # Confirmar los cambios en la base de datos
        conn.commit()

        # Devolver una respuesta exitosa
        return jsonify({"message": "Los equipos han sido creados correctamente"})

    except Exception as e:
        # En caso de error, realizar un rollback y devolver un mensaje de error
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()


@positions_bp.put("/positions")
def update_positions():
    conn = db()
    cursor = conn.cursor()

    try:
        data = request.get_json()

        # Obtener el ID de la liga y el nombre de la liga del objeto JSON
        league_id = data.get("league_id")
        league_name = data.get("league_name")

        # Actualizar la liga en la tabla "leagues"
        cursor.execute(
            "UPDATE leagues SET league_name = %s WHERE id = %s",
            (league_name, league_id),
        )

        # Obtener la lista de equipos del objeto JSON
        teams = data.get("teams")

        for team_data in teams:
            # Obtener los datos individuales del equipo
            team_id = team_data.get("team_id")
            team_name = team_data.get("team_name")
            position = team_data.get("position")
            matches_played = team_data.get("matches_played")
            games_won = team_data.get("games_won")
            games_drawn = team_data.get("games_drawn")
            games_lost = team_data.get("games_lost")
            goals_for = team_data.get("goals_for")
            goals_against = team_data.get("goals_against")
            points = team_data.get("points")

            # Actualizar el equipo en la tabla "teams"
            if team_id:
                cursor.execute(
                    "UPDATE teams SET team_name = %s, position = %s, matches_played = %s, games_won = %s, games_drawn = %s, games_lost = %s, goals_for = %s, goals_against = %s, points = %s WHERE id = %s",
                    (
                        team_name,
                        position,
                        matches_played,
                        games_won,
                        games_drawn,
                        games_lost,
                        goals_for,
                        goals_against,
                        points,
                        team_id,
                    ),
                )
            else:
                # Insertar un nuevo equipo en la tabla "teams"
                cursor.execute(
                    "INSERT INTO teams (team_name, position, matches_played, games_won, games_drawn, games_lost, goals_for, goals_against, points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        team_name,
                        position,
                        matches_played,
                        games_won,
                        games_drawn,
                        games_lost,
                        goals_for,
                        goals_against,
                        points,
                    ),
                )
                team_id = cursor.lastrowid

            # Actualizar la posición en la tabla "positions"
            cursor.execute(
                "UPDATE positions SET team_id = %s WHERE team_id = %s AND league_id = %s",
                (team_id, team_id, league_id),
            )

        # Confirmar los cambios en la base de datos
        conn.commit()

        # Devolver una respuesta exitosa
        return jsonify(
            {"message": "Las posiciones han sido actualizadas correctamente"}
        )

    except Exception as e:
        # En caso de error, realizar un rollback y devolver un mensaje de error
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()
