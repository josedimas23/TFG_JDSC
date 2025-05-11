#!/usr/bin/env bash
set -euo pipefail
CLUSTER_NAME="tfg"
REGISTRY_NAME="kind-registry"
REGISTRY_PORT="5000"

# 1) Arranca el registry local si no existe
if [ "$(docker ps -q -f name=${REGISTRY_NAME})" == "" ]; then
  docker run -d --restart=always -p ${REGISTRY_PORT}:5000 --name ${REGISTRY_NAME} registry:2
  echo "[+] Registry ${REGISTRY_NAME} en puerto ${REGISTRY_PORT} listo."
fi

# 2) Crea clúster kind con el registry ya configurado
kind create cluster --name ${CLUSTER_NAME} --config kind-config.yaml || true

# 3) Conecta el registry a la red 'kind' (por si no lo está)
if ! docker network inspect kind | grep -q ${REGISTRY_NAME}; then
  docker network connect kind ${REGISTRY_NAME} || true
fi

echo "[✔] Clúster kind '${CLUSTER_NAME}' y registry operativo."