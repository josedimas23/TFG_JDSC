#  Simulación y Gestión Escalable de Datos IoT en Entornos Privados mediante Contenedores Dinámicos

Es una plataforma contenerizada sobre **Kubernetes local (Kind)** que simula, ingiere, almacena y visualiza datos IoT. Incluye generación de datos simulados, API REST (Flask), base de datos CrateDB con volumen persistente, dashboards Grafana autocargados y autoscaling con HPA/ Metrics-Server. Todo el stack se levanta con un solo script.


## Requisitos (Probado en Ubuntu)

**Docker Engine**: Repositorio oficial + \`docker compose\` plugin


**Kind**: \`curl -Lo kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-$(uname)-amd64 && sudo mv kind /usr/local/bin/\` 


**kubectl**:  \`curl -LO "https://dl.k8s.io/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/$(uname | tr '[:upper:]' '[:lower:]')/amd64/kubectl"\` 

**Docker Desktop** en Windows/Mac funciona igual.


## Despliegue

```bash
./reset_and_redeploy.sh
```

El script realiza:

1. Destrucción del clúster anterior y del registry local.  
2. Arranque de \`kind-registry\` (puerto 5000) y creación del clúster Kind con mapeo de puertos (80/443).  
3. Construcción y push de las imágenes **flask-api** y **data-generator** al registry (\`TAG=1.1\`).  
4. Instalación del Metrics-Server parcheado y del controlador NGINX Ingress.  
5. Aplicación del manifiesto unificado \`K8s_full_stack_v2.yaml\` con todos los recursos.  
6. Carga del esquema SQL en CrateDB y reinicio controlado de Grafana.  

Espera ~2 min hasta que todos los pods estén \`Running\`. 


## Servicios disponibles

Primero añade en \`/etc/hosts\`:

```
127.0.0.1 api.tfg.local grafana.tfg.local crate.tfg.local
```

| Servicio | URL  | Descripción |
|----------|-----------------------------|-------------|
| **Grafana** | http://grafana.tfg.local | Dashboards (usuario: \`admin\` / \`123456j\`) |
| **CrateDB** | http://crate.tfg.local   | Base de datos |
| **API Flask** | http://api.tfg.local     | Endpoints |


## Uso rápido de la API

```bash
# insertar datos
curl -X POST http://api.tfg.local/data \
  -H "Content-Type: application/json" -H "X-API-KEY: 123456j" \
  -d @payload.json
# consultar datos
curl -G http://api.tfg.local/data \
  -H "X-API-KEY: 123456j" \
  --data-urlencode "id_casa=casa_001" \
  --data-urlencode "tipo_dato=temperatura"
```

\`payload.json\` de ejemplo esta en el repositorio.


## Comandos útiles

```bash
# Consulta de pods y nodo
kubectl get pods -n tfg-iot -o wide

# Metricas del autoscaling
kubectl get hpa -n tfg-iot

# Metricas en vivo
kubectl top pods -n tfg-iot

# Ver los logs de el pod que quieras
kubectl logs -n tfg-iot <pod>

# borrar clúster
kind delete cluster --name tfg
```


Proyecto desarrollado como Trabajo Fin de Grado en Ingeniería Informática – Universidad de Granada (2025) - Jose Dimas Sánchez Casas
