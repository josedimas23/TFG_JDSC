-- Datos IoT
CREATE TABLE IF NOT EXISTS iot_data (
  id        TEXT PRIMARY KEY,
  id_casa   TEXT,
  tipo_dato TEXT,
  id_sensor TEXT,
  valor     OBJECT(DYNAMIC),
  time      TIMESTAMP
);

-- Rangos por tipo (usado en validators.py)
CREATE TABLE IF NOT EXISTS iot_ranges (
  tipo_dato  TEXT PRIMARY KEY,
  min_val    DOUBLE,
  max_val    DOUBLE,
  color      TEXT
);

INSERT INTO iot_ranges (tipo_dato, min_val, max_val, color) VALUES
  ('temperatura', -10.0, 50.0, 'red'),
  ('saturacion_oxigeno', 80.0, 100.0, 'cyan'),
  ('humedad', 0.0, 100.0, 'blue'),
  ('heart_rate', 40.0, 180.0, 'orange'),
  ('posicion_x', 0.0, 100.0, 'green'),
  ('posicion_y', 0.0, 100.0, 'green'),
  ('certainty', 0.0, 1.0, 'gray'),
  ('binarios', 0, 1, 'purple');

