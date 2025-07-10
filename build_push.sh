#!/usr/bin/env bash
set -euo pipefail

# 1. Configuración luster kind

REGISTRY="registry.local:5000"   
CLUSTER_NAME="tfg"         
TAG="1.1"

# 2. Build imágenes 

echo "[+] Construyendo flask-api…"
docker build -t ${REGISTRY}/flask-api:${TAG} -f API/Dockerfile .

echo "[+] Construyendo data-generator…"
docker build -t ${REGISTRY}/data-generator:${TAG} -f data_generator/Dockerfile .

# 3. Push de las imágenes al registry local

echo "[+] Empujando al registry (${REGISTRY})…"
if curl -s http://${REGISTRY}/v2/ >/dev/null 2>&1; then
  docker push ${REGISTRY}/flask-api:${TAG}
  docker push ${REGISTRY}/data-generator:${TAG}
else
  echo "[!] Registry no accesible aún → asegúrate de que /etc/hosts contiene '127.0.0.1 registry.local' y el contenedor kind-registry está activo" && exit 1
fi

# 4. Si existe clúster kind con el nombre dado, cargamos imágenes dentro

if command -v kind >/dev/null 2>&1 && kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
  echo "[+] Inyectando imágenes en kind (${CLUSTER_NAME})…"
  kind load docker-image --name ${CLUSTER_NAME} ${REGISTRY}/flask-api:${TAG}
  kind load docker-image --name ${CLUSTER_NAME} ${REGISTRY}/data-generator:${TAG}
fi

echo "[✔] Imágenes listas"