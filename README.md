```bash
# Validación rápida de ETAPA 1

# 1. Construir e inyectar imágenes\ 
./build_push.sh

# 2. Arrancar stack con Compose (opcional)
docker compose --env-file .env.tfg up -d

# 3. Probar salud del API\ 
curl -H "X-API-KEY: 123456j" http://localhost:8080/api/health



# Validación rápida de ETAPA 2

cd ~/Escritorio/TFG_IOT
./setup_registry.sh

# Mostrar la info básica del clúster
kubectl cluster-info --context kind-tfg

# Ver nodos y su estado
kubectl get nodes -o wide
curl http://registry.local:5000/v2/_catalog

# (solo si hace falta recompilar/volver a subir)
./build_push.sh
curl http://registry.local:5000/v2/_catalog
# → { "repositories": ["flask-api","data-generator"] }



# Validación rápida de ETAPA 3

# 1. Instalar metrics-server e ingress
kubectl apply -f metrics-server.yaml
kubectl apply -f ingress-nginx.yaml

# 2. Esperar a que los pods estén Ready
kubectl get pods -n metrics-server -w
kubectl get pods -n ingress-nginx -w
kubectl get svc ingress-nginx-controller -n ingress-nginx   # 80:30550 / 443:31080

# 3. Verificar métricas
kubectl top nodes

# 4. Probar StorageClass
kubectl apply -f pvc-test.yaml
kubectl get pvc pvc-test
kubectl exec pvc-smoke-test -- cat /data/ok   # -> it-works



# Validación rápida de ETAPA 4

