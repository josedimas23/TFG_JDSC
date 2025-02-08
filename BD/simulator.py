# -*- coding: utf-8 -*-
import time
import random
import requests
import uuid 

# Configuración de CrateDB
CRATE_URL = "http://localhost:4200/_sql"

def generate_data():
    """Genera datos simulados de sensores IoT."""
    return {
        "id": str(uuid.uuid4()), 
        "sensor_id": f"sensor-{random.randint(1, 10)}",
        "temperature": round(random.uniform(18.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 70.0), 2),
        "co2": round(random.uniform(300.0, 800.0), 2),
    }

def insert_data(data):
    """Envía los datos a CrateDB mediante una consulta SQL."""
    query = {
        "stmt": "INSERT INTO iot_data (id, sensor_id, temperature, humidity, co2) VALUES (?, ?, ?, ?, ?)",
        "args": [data["id"], data["sensor_id"], data["temperature"], data["humidity"], data["co2"]]
    }
    
    response = requests.post(CRATE_URL, json=query)
    if response.status_code == 200:
        print(f" Datos insertados: {data}")
    else:
        print(f" Error al insertar: {response.text}")

if __name__ == "__main__":
    print("🚀 Iniciando simulador de datos IoT...")
    while True:
        data = generate_data()
        insert_data(data)
        time.sleep(5)  # Simula nuevos datos cada 5 segundos
