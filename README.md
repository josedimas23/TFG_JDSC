# Validación rápida de ETAPA 1

```bash
# 1. Construir e inyectar imágenes\ ./build_push.sh

# 2. Arrancar stack con Compose (opcional)
docker compose --env-file .env.tfg up -d

# 3. Probar salud del API\ ncurl -H "X-API-KEY: 123456j" http://localhost:8080/api/health