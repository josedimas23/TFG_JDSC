#!/usr/bin/env bash
set -euo pipefail

# Configuración
REGISTRY="registry.local:5000"
TAG="1.0"

# Build imágenes ------------------------------------------------

echo "[+] Construyendo flask-api…"
docker build -t ${REGISTRY}/flask-api:${TAG} -f API/Dockerfile .

echo "[+] Construyendo data-generator…"
docker build -t ${REGISTRY}/data-generator:${TAG} -f data_generator/Dockerfile .

# Push / load ---------------------------------------------------

echo "[+] Empujando al registry (${REGISTRY})…"
if curl -s http://${REGISTRY}/v2/ >/dev/null 2>&1; then
  docker push ${REGISTRY}/flask-api:${TAG}
  docker push ${REGISTRY}/data-generator:${TAG}
else
  echo "[!] Registry no accesible aún → solo build local"
fi

# Si existe clúster kind, cargamos imágenes dentro
if command -v kind >/dev/null 2>&1 && kind get clusters >/dev/null 2>&1; then
  echo "[+] Inyectando imágenes en kind…"
  kind load docker-image ${REGISTRY}/flask-api:${TAG}
  kind load docker-image ${REGISTRY}/data-generator:${TAG}
fi

echo "[✔] Imágenes listas"