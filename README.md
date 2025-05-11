# Validación rápida de ETAPA 1

```bash
# 1. Construir e inyectar imágenes\ ./build_push.sh

# 2. Arrancar stack con Compose (opcional)
docker compose --env-file .env.tfg up -d

# 3. Probar salud del API\ ncurl -H "X-API-KEY: 123456j" http://localhost:8080/api/health

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
