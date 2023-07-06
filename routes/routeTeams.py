from flask import Blueprint, jsonify, request
import json
from db import db

teams_bp = Blueprint("teams", __name__)


import json

@teams_bp.get("/teams")
def get_teams():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM teams")
    teams = cur.fetchall()
    cur.close()
    conn.close()

    # Convertir la lista de tuplas a una lista de diccionarios
    teams_json = [dict(zip(cur.column_names, team)) for team in teams]

    # Devolver la lista de objetos JSON
    return json.dumps(teams_json)



@teams_bp.post("/teams")
def post_team():
    conn = db()
    cursor = conn.cursor()
    # Obtener los datos del equipo desde el cuerpo de la solicitud
    data = request.get_json()
    # Extraer los campos del equipo
    team_name = data.get("team_name")
    # Verificar que se haya proporcionado el nombre del equipo
    if team_name is None:
        return jsonify({"error": "El nombre del equipo es obligatorio"}), 400

    try:
        # Insertar el equipo en la tabla "equipos"
        cursor.execute(
            "INSERT INTO teams (team_name) VALUES (%s)", (team_name,)
        )
        conn.commit()
        # Obtener el ID del equipo recién creado
        equipo_id = cursor.lastrowid
        # Devolver una respuesta con los datos del equipo creado
        response = {"id": equipo_id, "nombre_equipo": team_name}
        return jsonify(response), 201
    except Exception as e:
        # En caso de error, realizar un rollback y devolver un mensaje de error
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        conn.close()



@teams_bp.delete("/teams/<id>")
def delete_team(id):
    conn = db()
    try:
        # Crear un cursor para ejecutar las consultas
        cur = conn.cursor()
        # Ejecutar la consulta DELETE para eliminar el equipo por su ID
        cur.execute("DELETE FROM teams WHERE id = %s", (id,))
        # Confirmar los cambios en la base de datos
        conn.commit()
        # Cerrar el cursor
        cur.close()
        # Devolver una respuesta exitosa
        return jsonify({'message': 'El equipo ha sido eliminado correctamente'})
    except Exception as e:
        # En caso de error, realizar un rollback y devolver un mensaje de error
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()
