#!/usr/bin/env bash
set -euo pipefail

# 1. Borrar clúster anterior
kind delete cluster --name tfg

docker stop kind-registry && docker rm kind-registry 2>/dev/null || true

# 2. Crear nuevo clúster con puertos mapeados
./setup_registry.sh

# 3. Reconstruir e inyectar imágenes
TAG=1.1 ./build_push.sh   

# 4-A. Limpiar metrics-server anterior (por si acaso)
kubectl delete -n kube-system deploy/metrics-server svc/metrics-server --ignore-not-found

# 4-B. Instalar metrics-server parcheado
curl -sLo metrics-server.yaml https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
sed -i '/--kubelet-preferred-address-types=.*/a\        - --kubelet-insecure-tls' metrics-server.yaml
kubectl apply -f metrics-server.yaml

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.9.5/deploy/static/provider/kind/deploy.yaml

# etiqueta nodos para que el Ingress Controller pueda programarse en ambos
kubectl label node tfg-control-plane ingress-ready=true --overwrite
kubectl label node tfg-worker        ingress-ready=true --overwrite
kubectl label node tfg-worker2        ingress-ready=true --overwrite

# espera a que el controller esté OK
for i in {1..24}; do
  kubectl get pods -n ingress-nginx | grep ingress-nginx-controller | grep -q "1/1" && break
  echo "⏳ Esperando a que ingress-nginx-controller esté listo…"
  sleep 10
done || echo "⚠️ Timeout: el controlador aún no está Ready. Revisa con kubectl get pods -n ingress-nginx"

kubectl apply -f K8s/namespace.yaml
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
kubectl apply -f K8s/grafana-dashboard-iot-configmap.yaml
kubectl apply -f K8s/K8s_full_stack_v2.yaml


### 6. Esperar a CrateDB y cargar esquema --------------------------------------
kubectl wait --for=condition=ready pod/cratedb-0 -n tfg-iot --timeout=240s
kubectl cp ./BD/cratedb.sql tfg-iot/cratedb-0:/tmp/cratedb.sql
kubectl exec -n tfg-iot cratedb-0 -- bash -c "crash < /tmp/cratedb.sql"

kubectl rollout restart deployment grafana -n tfg-iot

### 7. Puertos de desarrollo ---------------------------------------
for i in {1..6}; do
  if kubectl top pods -n tfg-iot &>/dev/null; then
    echo '✅ Metrics API disponible.'
    break
  fi
  echo '⏳ Esperando a metrics-server…'
  sleep 10
done || echo '⚠️  Metrics API aún no disponible; comprueba en unos segundos.'
echo "  • API     → http://api.tfg.local:/health"
echo "  • Grafana → http://grafana.tfg.local/"
echo "  • CrateDB → http://crate.tfg.local/"
