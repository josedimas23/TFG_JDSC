from flask import Flask, request, jsonify
import requests
import uuid
import random

app = Flask(__name__)
CRATE_URL = "http://cratedb:4200/_sql"  # Nombre del servicio en Docker

def generate_data():
    """Genera datos simulados de sensores IoT."""
    return {
        "id": str(uuid.uuid4()), 
        "sensor_id": f"sensor-{random.randint(1, 10)}",
        "temperature": round(random.uniform(18.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 70.0), 2),
        "co2": round(random.uniform(300.0, 800.0), 2),
    }

@app.route('/data', methods=['POST'])
def insert_data():
    if request.is_json:
        try:
            data = request.get_json()
            # Si data es un diccionario, lo convertimos en una lista con un solo elemento
            if isinstance(data, dict):
                data = [data]
            # Validar que data es una lista de diccionarios
            if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
                return jsonify({"error": "Formato de datos incorrecto"}), 400
            # Validar cada conjunto de datos en la lista
            for item in data:
                if not all(key in item for key in ("id", "sensor_id", "temperature", "humidity", "co2")):
                    return jsonify({"error": "Datos incompletos"}), 400
                if not isinstance(item["id"], str) or not isinstance(item["sensor_id"], str):
                    return jsonify({"error": "Tipos de datos incorrectos"}), 400
                if not isinstance(item["temperature"], (int, float)) or not isinstance(item["humidity"], (int, float)) or not isinstance(item["co2"], (int, float)):
                    return jsonify({"error": "Tipos de datos incorrectos"}), 400
        except Exception as e:
            return jsonify({"error": "Error al procesar JSON", "details": str(e)}), 400
    else:
        data = [generate_data()]  # Genera un solo conjunto de datos simulados si no se envía JSON

    # Insertar cada conjunto de datos en la base de datos
    for item in data:
        query = {
            "stmt": "INSERT INTO iot_data (id, sensor_id, temperature, humidity, co2) VALUES (?, ?, ?, ?, ?)",
            "args": [item["id"], item["sensor_id"], item["temperature"], item["humidity"], item["co2"]]
        }
        response = requests.post(CRATE_URL, json=query)
        if response.status_code != 200:
            return jsonify({"error": "Error al insertar", "details": response.text}), 500

    return jsonify({"message": "Datos insertados", "data": data}), 200

@app.route('/data/all', methods=['GET'])
def get_all_data():
    """Recupera todos los datos de la base de datos."""
    query = {"stmt": "SELECT * FROM iot_data"}
    response = requests.post(CRATE_URL, json=query)
    
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Error al recuperar datos", "details": response.text}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
