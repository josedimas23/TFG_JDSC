from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import uuid
from validators import register_error_handlers, ValidationError, validate_data_payload
from utils import chunk_list
from functools import wraps
load_dotenv()

app = Flask(__name__)

# Variables de entorno
CRATE_USER = os.getenv("CRATE_USER")
CRATE_PASSWORD = os.getenv("CRATE_PASSWORD")
CRATE_HOST = os.getenv("CRATE_HOST")
API_KEY = os.getenv("API_KEY", "123456j")
MAX_BULK_SIZE = 500

CRATE_URL = f"http://{CRATE_USER}:{CRATE_PASSWORD}@{CRATE_HOST}/_sql"

register_error_handlers(app)

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('X-API-KEY')
        if not key or key != API_KEY:
            return jsonify({"success": False, "error": {"type": "Unauthorized", "message": "API Key inválida o faltante"}}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/data', methods=['POST'])
@require_api_key
def insert_data():
    if not request.is_json:
        raise ValidationError("Debe ser JSON.")

    payload = request.get_json()
    if not isinstance(payload, list):
        raise ValidationError("Se esperaba una lista JSON.")

    bulk_args = []
    query = """
        INSERT INTO iot_data (id, id_casa, tipo_dato, id_sensor, valor, time)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    for data in payload:
        validated_data = validate_data_payload(data)
        bulk_args.append([
            str(uuid.uuid4()),
            validated_data["id_casa"],
            validated_data["tipo_dato"],
            validated_data["id_sensor"],
            validated_data["valor"],
            validated_data["time"]
        ])

    for batch in chunk_list(bulk_args, MAX_BULK_SIZE):
        response = requests.post(CRATE_URL, json={"stmt": query, "bulk_args": batch})
        if response.status_code != 200:
            raise Exception("Error en CrateDB:", response.text)

    return jsonify({"success": True, "message": "Insertado correctamente."}), 200

@app.route('/data', methods=['GET'])
@require_api_key
def get_data():
    tipo_dato = request.args.get('tipo_dato')
    id_casa = request.args.get('id_casa')

    if not tipo_dato or not id_casa:
        raise ValidationError("Parámetros 'tipo_dato' y 'id_casa' requeridos.")

    query = {
        "stmt": "SELECT * FROM iot_data WHERE tipo_dato = ? AND id_casa = ? ORDER BY time ASC",
        "args": [tipo_dato, id_casa]
    }

    response = requests.post(CRATE_URL, json=query)
    if response.status_code != 200:
        raise Exception("Error al obtener datos:", response.text)

    return jsonify({"success": True, "data": response.json()}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"success": True, "status": "ok"}), 200

# --- Ruta de salud con prefijo /api (necesario para el Ingress) ----
@app.route('/api/health', methods=['GET'])
def api_health():
    return health()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

