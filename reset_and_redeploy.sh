#!/usr/bin/env bash
set -euo pipefail

# 1. Borrar clúster anterior
kind delete cluster --name tfg

docker stop kind-registry && docker rm kind-registry 2>/dev/null || true

# 2. Crear nuevo clúster con puertos mapeados
./setup_registry.sh

# 3. Reconstruir e inyectar imágenes
TAG=1.1 ./build_push.sh   

### 4. Métricas + Ingress (manifests oficiales) -------------------------------
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.9.5/deploy/static/provider/kind/deploy.yaml

# etiqueta nodos para que el Ingress Controller pueda programarse en ambos
kubectl label node tfg-control-plane ingress-ready=true --overwrite
kubectl label node tfg-worker        ingress-ready=true --overwrite

# espera a que el controller esté OK
kubectl wait -n ingress-nginx --for=condition=ready pod -l app.kubernetes.io/component=controller --timeout=180s

### 5. Desplegar TODO el stack (manifiesto único) ------------------------------
kubectl apply -f K8s/K8s_full_stack_v2.yaml

### 6. Esperar a CrateDB y cargar esquema --------------------------------------
kubectl wait --for=condition=ready pod/cratedb-0 -n tfg-iot --timeout=240s
kubectl cp ./BD/cratedb.sql tfg-iot/cratedb-0:/tmp/cratedb.sql
kubectl exec -n tfg-iot cratedb-0 -- bash -c "crash < /tmp/cratedb.sql"

### 7. Puertos de desarrollo ---------------------------------------
echo -e "\nℹ️  Añade a /etc/hosts:"
echo "127.0.0.1  api.tfg.local grafana.tfg.local crate.tfg.local"
echo -e "\n🔗  Endpoints locales (via Ingress @30080):"
echo "  • API     → http://api.tfg.local:30080/health"
echo "  • Grafana → http://grafana.tfg.local:30080/"
echo "  • CrateDB → http://crate.tfg.local:30080/"
echo -e "\n▶ Para port-forward directo:"
echo "  kubectl port-forward -n tfg-iot svc/grafana 13000:3000 &"
echo "  kubectl port-forward -n tfg-iot svc/cratedb 14200:4200 &"
