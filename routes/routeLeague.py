from flask import Blueprint, jsonify, request
import json
from db import db

league_bp = Blueprint("league", __name__)


@league_bp.get("/league")
def get_league():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM leagues")
    leagues = cur.fetchall()
    cur.close()
    conn.close()
    # Convertir la lista de tuplas a una lista de diccionarios
    league_json = [dict(zip(cur.column_names, league)) for league in leagues]

    # Devolver la lista de objetos JSON
    return json.dumps(league_json)


@league_bp.post("/league")
def post_league():
    conn = db()
    cursor = conn.cursor()
    # Obtener los datos del equipo desde el cuerpo de la solicitud
    data = request.get_json()
    # Extraer los campos del equipo
    league_name = data.get("league_name")
    # Verificar que se haya proporcionado el nombre del equipo
    if league_name is None:
        return jsonify({"error": "El nombre de la liga es obligatorio"}), 400

    try:
        # Insertar el equipo en la tabla "equipos"
        cursor.execute("INSERT INTO leagues (league_name) VALUES (%s)", (league_name,))
        conn.commit()
        # Obtener el ID del equipo recién creado
        league_id = cursor.lastrowid
        # Devolver una respuesta con los datos del equipo creado
        response = {"id": league_id, "nombre_equipo": league_name}
        return jsonify(response), 201
    except Exception as e:
        # En caso de error, realizar un rollback y devolver un mensaje de error
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        conn.close()


@league_bp.delete("/league/<id>")
def delete_league(id):
    conn = db()
    try:
        # Crear un cursor para ejecutar las consultas
        cur = conn.cursor()
        # Ejecutar la consulta DELETE para eliminar el equipo por su ID
        cur.execute("DELETE FROM leagues WHERE id = %s", (id,))
        # Confirmar los cambios en la base de datos
        conn.commit()
        # Cerrar el cursor
        cur.close()
        # Devolver una respuesta exitosa
        return jsonify({"message": "La liga ha sido eliminado correctamente"})
    except Exception as e:
        # En caso de error, realizar un rollback y devolver un mensaje de error
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()
