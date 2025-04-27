from flask import Flask, request, jsonify
import requests

# Importamos las funciones de validación
from validators import (
    validate_binarios,
    validate_heart_rate,
    validate_posicion,
    validate_saturacion_oxigeno,
    validate_temperatura
)


app = Flask(__name__)
CRATE_URL = "http://cratedb:4200/_sql"  # Nombre del servicio en Docker

# def generate_data():
#     """Genera datos simulados de sensores IoT."""
#     return {
#         "id": str(uuid.uuid4()), 
#         "sensor_id": f"sensor-{random.randint(1, 10)}",
#         "temperature": round(random.uniform(18.0, 30.0), 2),
#         "humidity": round(random.uniform(30.0, 70.0), 2),
#         "co2": round(random.uniform(300.0, 800.0), 2),
#     }

class ValidationError(Exception):
    pass

# Handlers globales de errores
@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({"success": False, "error": {"type": "ValidationError", "message": str(e)}}), 400

@app.errorhandler(404)
def handle_404_error(e):
    return jsonify({"success": False, "error": {"type": "NotFound", "message": "Recurso no encontrado."}}), 404

@app.errorhandler(500)
def handle_500_error(e):
    return jsonify({"success": False, "error": {"type": "InternalServerError", "message": "Error interno del servidor."}}), 500

@app.route('/data', methods=['POST'])
def insert_data():
    data_type = request.args.get('type')
    if not data_type:
        raise ValidationError("Tipo de datos no especificado.")

    if not request.is_json:
        raise ValidationError("Formato de datos incorrecto: no es JSON.")

    data_list = request.get_json()
    if not isinstance(data_list, list):
        raise ValidationError("Formato de datos incorrecto: se esperaba una lista.")

    bulk_args = []
    query = ""

    for data in data_list:
       
        if data_type == "binarios":
            validate_binarios(data)
            bulk_args.append([data["TIME"], data["closet_2"]])
            query = "INSERT INTO binarios_data (TIME, closet_2) VALUES (?, ?)"
        elif data_type == "heart_rate":
            validate_heart_rate(data)
            bulk_args.append([data["TIME"], float(data["heart_rate"])])
            query = "INSERT INTO heart_rate_data (TIME, heart_rate) VALUES (?, ?)"
        elif data_type == "posicion":
            validate_posicion(data)
            bulk_args.append([data["TIME"], data["x1"], data["y1"], data["x2"], data["y2"], data["certainty"]])
            query = "INSERT INTO posicion_data (TIME, x1, y1, x2, y2, certainty) VALUES (?, ?, ?, ?, ?, ?)"
        elif data_type == "saturacion_oxigeno":
            validate_saturacion_oxigeno(data)
            bulk_args.append([data["TIME"], data["oxygen_saturation"]])
            query = "INSERT INTO saturacion_oxigeno_data (TIME, oxygen_saturation) VALUES (?, ?)"
        elif data_type == "temperatura":
            validate_temperatura(data)
            bulk_args.append([data["TIME"], data["temperature"]])
            query = "INSERT INTO temperatura_data (TIME, temperature) VALUES (?, ?)"
        else:
            raise ValidationError("Tipo de datos no soportado.")

    if bulk_args:
        response = requests.post(CRATE_URL, json={"stmt": query, "bulk_args": bulk_args})
        if response.status_code != 200:
            raise Exception("Error al insertar datos en la base de datos.")

    return jsonify({"success": True, "message": "Datos insertados", "data": data_list}), 200

@app.route('/data/all', methods=['GET'])
def get_all_data():
    """Recupera todos los datos de la base de datos."""
    query = {"stmt": "SELECT * FROM binarios_data UNION ALL SELECT * FROM heart_rate_data UNION ALL SELECT * FROM posicion_data UNION ALL SELECT * FROM saturacion_oxigeno_data UNION ALL SELECT * FROM temperatura_data"}
    response = requests.post(CRATE_URL, json=query)
    
    if response.status_code == 200:
        return jsonify({"success": True, "data": response.json()}), 200
    else:
        raise Exception("Error al recuperar datos de la base de datos.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# curl -X POST "http://localhost:5000/data?type=temperatura" -H "Content-Type: application/json" -d @data.json
# curl -X GET "http://localhost:5000/data/all"
