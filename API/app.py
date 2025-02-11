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
        data = request.get_json()
    else:
        data = generate_data()  # Genera datos simulados si no se envía JSON
    query = {
        "stmt": "INSERT INTO iot_data (id, sensor_id, temperature, humidity, co2) VALUES (?, ?, ?, ?, ?)",
        "args": [data["id"], data["sensor_id"], data["temperature"], data["humidity"], data["co2"]]
    }
    response = requests.post(CRATE_URL, json=query)
    
    if response.status_code == 200:
        return jsonify({"message": "Datos insertados", "data": data}), 200
    else:
        return jsonify({"error": "Error al insertar", "details": response.text}), 500

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
