import requests
import uuid
import random
import time

API_URL = "http://flask-api:5000/data"  # Usa el nombre del servicio de Flask en Docker

def generate_data():
    """Genera datos aleatorios simulados de sensores IoT."""
    return {
        "id": str(uuid.uuid4()),
        "sensor_id": f"sensor-{random.randint(1, 10)}",
        "temperature": round(random.uniform(18.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 70.0), 2),
        "co2": round(random.uniform(300.0, 800.0), 2),
    }

def send_data():
    """Envía datos cada 5 segundos."""
    while True:
        data = generate_data()
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(API_URL, json=data, headers=headers)
            if response.status_code == 200:
                print(f" Datos enviados: {data}")
            else:
                print(f" Error al enviar: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f" Error de conexión: {e}")

        time.sleep(10)  # Cambia este valor si quieres otro intervalo

if __name__ == "__main__":
    send_data()
