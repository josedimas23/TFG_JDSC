# syntax=docker/dockerfile:1

# PARTE 1
FROM python:3.11-slim AS builder
WORKDIR /app

# Dependencias Python
COPY API/requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiamos código
COPY API/ ./
# Ejecuta pytest si existe carpeta tests (no detiene build si no la hay)
RUN if [ -d "tests" ]; then python -m pytest -q; else echo "No tests"; fi

# PARTE 2
FROM python:3.11-slim
WORKDIR /app

# Copiamos todo el entorno Python del builder
COPY --from=builder /usr/local /usr/local

# Copiamos ÚNICAMENTE el código fuente de la API
COPY API/ ./

EXPOSE 5000
ENV PYTHONUNBUFFERED=1
CMD ["python", "app.py"]