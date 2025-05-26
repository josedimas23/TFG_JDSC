# reset_and_redeploy.sh

# 1. Borrar clúster anterior
kind delete cluster --name tfg

docker stop kind-registry && docker rm kind-registry 2>/dev/null || true

# 2. Crear nuevo clúster con puertos mapeados
./setup_registry.sh

# 3. Reconstruir e inyectar imágenes
TAG=1.1 ./build_push.sh

# 4. Aplicar manifiestos básicos
kubectl apply -f K8s/namespace.yaml

# 4.1 Instalar Metrics Server para kind/local
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl patch deployment metrics-server -n kube-system --type=json \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'

# 4.2 Ingress NGINX
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.9.5/deploy/static/provider/kind/deploy.yaml

# Añadir etiquetas necesarias para programar el Ingress Controller
kubectl label node tfg-control-plane ingress-ready=true --overwrite
kubectl label node tfg-worker ingress-ready=true --overwrite

# Esperar a que ingress-nginx esté operativo
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=180s

# 5. Desplegar aplicación IoT
kubectl apply -f K8s/cratedb-statefulset.yaml
kubectl apply -f K8s/flask-api-deployment.yaml
kubectl apply -f K8s/data-generator-deployment.yaml
kubectl apply -f K8s/grafana-deployment.yaml
kubectl apply -f K8s/flask-api-hpa.yaml

# 6. Aplicar Ingress para API (opcional para despliegue con DNS)
# kubectl apply -f K8s/ingress-api.yaml
# kubectl apply -f K8s/ingress-grafana.yaml
# kubectl apply -f K8s/ingress-cratedb.yaml

# 7. Inicializar tablas en CrateDB automáticamente
kubectl wait --for=condition=ready pod/cratedb-0 -n tfg-iot --timeout=240s
kubectl cp ./BD/cratedb.sql tfg-iot/cratedb-0:/tmp/cratedb.sql
kubectl exec -n tfg-iot cratedb-0 -- bash -c "crash < /tmp/cratedb.sql"

# 8. Port-forward de servicios para acceso local

# kubectl port-forward -n tfg-iot svc/grafana 13000:3000 

# kubectl port-forward -n tfg-iot svc/cratedb 14200:4200 

# kubectl port-forward -n tfg-iot svc/flask-api 15000:5000 

echo "✅ Accede a Grafana en:   http://localhost:13000"
echo "✅ Accede a CrateDB en:   http://localhost:14200"
echo "✅ Accede a API en:       http://localhost:15000/api/health"
