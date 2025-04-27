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
    if "TIME" not in data or "closet_2" not in data:
        raise ValueError("Faltan campos 'TIME' o 'closet_2'.")
    if not isinstance(data["TIME"], str):
        raise ValueError("El campo 'TIME' debe ser una cadena.")
    if not isinstance(data["closet_2"], (int, bool)):
        raise ValueError("El campo 'closet_2' debe ser un entero o booleano.")

def validate_heart_rate(data):
    if "TIME" not in data or "heart_rate" not in data:
        raise ValueError("Faltan campos 'TIME' o 'heart_rate'.")
    if not isinstance(data["TIME"], str):
        raise ValueError("El campo 'TIME' debe ser una cadena.")
    if not isinstance(data["heart_rate"], (int, float)):
        raise ValueError("El campo 'heart_rate' debe ser numérico.")

def validate_posicion(data):
    required_fields = ["TIME", "x1", "y1", "x2", "y2", "certainty"]
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
    if not isinstance(data["oxygen_saturation"], (int, float)):
        raise ValueError("El campo 'oxygen_saturation' debe ser numérico.")

def validate_temperatura(data):
    if "TIME" not in data or "temperature" not in data:
        raise ValueError("Faltan campos 'TIME' o 'temperature'.")
    if not isinstance(data["TIME"], str):
        raise ValueError("El campo 'TIME' debe ser una cadena.")
    if not isinstance(data["temperature"], (int, float)):
        raise ValueError("El campo 'temperature' debe ser numérico.")


