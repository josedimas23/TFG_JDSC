from flask import jsonify

class ValidationError(Exception):
    """Error personalizado para validaciones."""
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


def validate_binarios(data):
    if "TIME" not in data:
        raise ValueError("Falta el campo 'TIME'.")
    if not isinstance(data["TIME"], str):
        raise ValueError("El campo 'TIME' debe ser una cadena.")

    boolean_fields = [
        "closet_2", "closet_3", "closet_4", "dishes_9", "fridge_13",
        "hum_shower_25", "micro_5", "pans_8", "shower_24_apertura",
        "shower_31", "sink_21", "tap_22", "wc_17"
    ]
    numeric_fields = [
        "pc_1_current_consumption", "tv_30_current_consumption"
    ]

    for field in boolean_fields + numeric_fields:
        if field not in data:
            raise ValueError(f"Falta el campo '{field}'.")

    for field in boolean_fields:
        if not isinstance(data[field], (bool, int)):
            raise ValueError(f"El campo '{field}' debe ser booleano o entero.")

    for field in numeric_fields:
        if not isinstance(data[field], (int, float)):
            raise ValueError(f"El campo '{field}' debe ser numérico.")
    
def validate_heart_rate(data):
    print("VALIDADOR HEART_RATE ACTUAL USADO") 
    if "TIME" not in data or "heart_rate" not in data:
        raise ValueError("Faltan campos 'TIME' o 'heart_rate'.")
    if not isinstance(data["TIME"], str):
        raise ValueError("El campo 'TIME' debe ser una cadena.")
    try:
        float(data["heart_rate"])
    except (ValueError, TypeError):
        raise ValueError("El campo 'heart_rate' debe ser convertible a numérico.")

def validate_posicion(data):
    required_fields = ["TIME", "X1", "Y1", "X2", "Y2", "certainty"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Falta el campo '{field}'.")
        if field != "TIME" and not isinstance(data[field], (int, float)):
            raise ValueError(f"El campo '{field}' debe ser numérico.")
    if not isinstance(data["TIME"], str):
        raise ValueError("El campo 'TIME' debe ser una cadena.")

def validate_saturacion_oxigeno(data):
    if "TIME" not in data or "oxygen_saturation" not in data:
        raise ValueError("Faltan campos 'TIME' o 'oxygen_saturation'.")
    if not isinstance(data["TIME"], str):
        raise ValueError("El campo 'TIME' debe ser una cadena.")
    try:
        data["oxygen_saturation"] = float(data["oxygen_saturation"])
    except ValueError:
        raise ValueError("El campo 'oxygen_saturation' debe ser numérico (aunque esté como string).")

def validate_temperatura(data):
    if "TIME" not in data or "temperature" not in data:
        raise ValueError("Faltan campos 'TIME' o 'temperature'.")
    if not isinstance(data["TIME"], str):
        raise ValueError("El campo 'TIME' debe ser una cadena.")
    try:
        data["temperature"] = float(data["temperature"])
    except ValueError:
        raise ValueError("El campo 'temperature' debe ser numérico (aunque esté como string).")

