import requests, os, random, time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = "123456j"
API_URL = os.getenv("API_URL")


headers = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY
}


def generar_dato():
    tipos = ['temperatura', 'saturacion_oxigeno', 'humedad', 'heart_rate', 'posicion', 'binarios']
    tipo = random.choice(tipos)

    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

    data = {
        "id_casa": f"casa_{random.randint(1,5):03d}",
        "tipo_dato": tipo,
        "id_sensor": f"{tipo}_sensor_{random.randint(1,5)}",
        "valor": {},
        "time": timestamp
    }

    if tipo == "temperatura":
        data["valor"] = {"temperature": round(random.uniform(-10,50),2)}
    elif tipo == "saturacion_oxigeno":
        data["valor"] = {"oxygen_saturation": round(random.uniform(80,100),2)}
    elif tipo == "humedad":
        data["valor"] = {"humidity": round(random.uniform(0,100),2)}
    elif tipo == "heart_rate":
        data["valor"] = {"heart_rate": random.randint(40,180)}
    elif tipo == "posicion":
        data["valor"] = {
            "x1": round(random.uniform(0,100),2),
            "y1": round(random.uniform(0,100),2),
            "x2": round(random.uniform(0,100),2),
            "y2": round(random.uniform(0,100),2),
            "certainty": round(random.uniform(0,1),2)
        }
    if tipo == "binarios":
        data["id_sensor"] = "multiple"
        data["valor"] = {f"sensor_{i}": random.randint(0,1) for i in range(1, 10)}
    else:
        data["id_sensor"] = f"{tipo}_sensor_{random.randint(1,5)}"

    return [data]

def enviar_datos():
    dato = generar_dato()
    try:
        response = requests.post(API_URL, headers=headers, json=dato)
        if response.status_code == 200:
            print(f"Dato insertado correctamente: {dato}")
        else:
            print(f"Error en la inserción: {response.text}")
    except Exception as e:
        print(f"Error de conexión con API: {e}")

if __name__ == "__main__":
    while True:
        enviar_datos()
        time.sleep(3)  # Inserta datos cada 3 segundos