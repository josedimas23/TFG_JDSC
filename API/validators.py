from flask import jsonify
import requests, os
from dotenv import load_dotenv

load_dotenv()
CRATE_USER = os.getenv("CRATE_USER")
CRATE_PASSWORD = os.getenv("CRATE_PASSWORD")
CRATE_HOST = os.getenv("CRATE_HOST")
CRATE_URL = f"http://{CRATE_USER}:{CRATE_PASSWORD}@{CRATE_HOST}/_sql"

class ValidationError(Exception):
    pass

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({"success": False, "error": {"type": "ValidationError", "message": str(e)}}), 400

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({"success": False, "error": {"type": "NotFound", "message": "Recurso no encontrado."}}), 404

    @app.errorhandler(500)
    def handle_500_error(e):
        return jsonify({"success": False, "error": {"type": "InternalServerError", "message": "Error interno del servidor."}}), 500

def obtener_rangos(tipo_dato):
    query = {
        "stmt": "SELECT min_val, max_val FROM iot_ranges WHERE tipo_dato = ?",
        "args": [tipo_dato]
    }
    response = requests.post(CRATE_URL, json=query)
    if response.status_code == 200 and response.json()["rows"]:
        min_val, max_val = response.json()["rows"][0]
        return min_val, max_val
    else:
        raise ValidationError(f"Rangos no definidos para '{tipo_dato}'.")

def validate_data_payload(data):
    required_fields = ["id_casa", "tipo_dato", "id_sensor", "valor", "time"]
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Falta el campo '{field}'.")

    tipo_dato = data["tipo_dato"]
    valor = data["valor"]

    if tipo_dato in ["temperatura", "saturacion_oxigeno", "humedad", "heart_rate"]:
        if len(valor) != 1:
            raise ValidationError(f"{tipo_dato} debe tener exactamente un campo.")
        
        campo, valor_num = next(iter(valor.items()))
        if not isinstance(valor_num, (int, float)):
            raise ValidationError(f"'{campo}' debe ser numérico.")

        min_val, max_val = obtener_rangos(tipo_dato)
        if not (min_val <= valor_num <= max_val):
            raise ValidationError(f"'{campo}' ({valor_num}) fuera de rango [{min_val}, {max_val}].")

    elif tipo_dato == "posicion":
        for coord in ["x1", "y1", "x2", "y2", "certainty"]:
            if coord not in valor or not isinstance(valor[coord], (int, float)):
                raise ValidationError(f"'{coord}' incorrecto o faltante.")
            tipo_rango = "certainty" if coord == "certainty" else f"posicion_{coord[0]}"
            min_val, max_val = obtener_rangos(tipo_rango)
            if not (min_val <= valor[coord] <= max_val):
                raise ValidationError(f"'{coord}' ({valor[coord]}) fuera de rango [{min_val}, {max_val}].")

    elif tipo_dato == "binarios":
        for campo, val in valor.items():
            if val not in [0, 1]:
                raise ValidationError(f"'{campo}' debe ser 0 o 1.")

    return data

# INSERT INTO iot_ranges (tipo_dato, min_val, max_val, color) VALUES
#   ('temperatura', -10.0, 50.0, 'red'),
#   ('saturacion_oxigeno', 80.0, 100.0, 'cyan'),
#   ('humedad', 0.0, 100.0, 'blue'),
#   ('heart_rate', 40.0, 180.0, 'orange'),
#   ('posicion_x', 0.0, 100.0, 'green'),
#   ('posicion_y', 0.0, 100.0, 'green'),
#   ('certainty', 0.0, 1.0, 'gray'),
#   ('binarios', 0, 1, 'purple');