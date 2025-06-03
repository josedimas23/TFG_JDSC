import json
from datetime import datetime, timedelta

base = datetime.strptime("2025-05-29T17:00:00", "%Y-%m-%dT%H:%M:%S")

payload = []
for i in range(1000):
    timestamp = base + timedelta(seconds=i)
    payload.append({
        "id_casa": "casa_001",
        "tipo_dato": "temperatura",
        "id_sensor": "sensor_1",
        "valor": { "temperatura": 20 + i % 5 },
        "time": timestamp.strftime("%Y-%m-%dT%H:%M:%S")
    })

with open("test_payload.json", "w") as f:
    json.dump(payload, f, indent=2)
