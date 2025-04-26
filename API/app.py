from flask import Flask, request, jsonify
import requests
import uuid
import random

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

@app.route('/data', methods=['POST'])
def insert_data():
    
    data_type = request.args.get('type')
    if not data_type:
        return jsonify({"error": "Tipo de datos no especificado"}), 400

    if request.is_json:
        data_list = request.get_json()
        if not isinstance(data_list, list):
            return jsonify({"error": "Formato de datos incorrecto"}), 400

        bulk_args = []
        for data in data_list:
            try:
                if data_type == "binarios":
                    bulk_args.append([data["time"], data["closet_2"]])
                    query = "INSERT INTO binarios_data (time, closet_2) VALUES (?, ?)"
                elif data_type == "heart_rate":
                    bulk_args.append([data["time"], data["heart_rate"]])
                    query = "INSERT INTO heart_rate_data (time, heart_rate) VALUES (?, ?)"
                elif data_type == "posicion":
                    bulk_args.append([data["time"], data["x1"], data["y1"], data["x2"], data["y2"], data["certainty"]])
                    query = "INSERT INTO posicion_data (time, x1, y1, x2, y2, certainty) VALUES (?, ?, ?, ?, ?, ?)"
                elif data_type == "saturacion_oxigeno":
                    bulk_args.append([data["time"], data["oxygen_saturation"]])
                    query = "INSERT INTO saturacion_oxigeno_data (time, oxygen_saturation) VALUES (?, ?)"
                elif data_type == "temperatura":
                    bulk_args.append([data["time"], data["temperature"]])
                    query = "INSERT INTO temperatura_data (time, temperature) VALUES (?, ?)"
                else:
                    return jsonify({"error": "Tipo de datos no soportado"}), 400
            except KeyError as e:
                return jsonify({"error": f"Campo faltante: {str(e)}"}), 400

        if bulk_args:
            response = requests.post(CRATE_URL, json={"stmt": query, "bulk_args": bulk_args})
            if response.status_code != 200:
                return jsonify({"error": "Error al insertar", "details": response.text}), 500

        return jsonify({"message": "Datos insertados", "data": data_list}), 200
    else:
        return jsonify({"error": "Formato de datos incorrecto"}), 400

@app.route('/data/all', methods=['GET'])
def get_all_data():
    """Recupera todos los datos de la base de datos."""
    query = {"stmt": "SELECT * FROM binarios_data UNION ALL SELECT * FROM heart_rate_data UNION ALL SELECT * FROM posicion_data UNION ALL SELECT * FROM saturacion_oxigeno_data UNION ALL SELECT * FROM temperatura_data"}
    response = requests.post(CRATE_URL, json=query)
    
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Error al recuperar datos", "details": response.text}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# curl -X POST "http://localhost:5000/data?type=temperatura" -H "Content-Type: application/json" -d @data.json
# curl -X GET "http://localhost:5000/data/all"
