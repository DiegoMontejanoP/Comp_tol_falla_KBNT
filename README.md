![01](https://drive.google.com/uc?id=1IjnYrdJXZ-okqe_uygSX1NM_1f3I-FVC)
![02](https://drive.google.com/uc?id=1VTWGVq4wPyIiJhLus8jiJ327UAvgDOaY)
![03](https://drive.google.com/uc?id=1jSRheqpygvJ7qKwOnnh4n0jG1-BZjWYP)
![04](https://drive.google.com/uc?id=1bOvcvoNJVcEh6u6ZtIbW5FIrbObhVrP9)

# 📖 Descripción

Este proyecto es una calculadora distribuida construida con una arquitectura de microservicios, donde cada operación matemática (suma, resta, multiplicación, división) es un servicio independiente desplegado en Kubernetes. Incluye un dashboard de visualización en tiempo real para monitorear el rendimiento y uso de los servicios.
## 🏗️ Arquitectura
Componentes del Sistema
- GUI Service: Interfaz web principal (Puerto 5000)
- Addition Service: Servicio de suma (Puerto 5001)
- Subtraction Service: Servicio de resta (Puerto 5002)
- Multiplication Service: Servicio de multiplicación (Puerto 5003)
- Division Service: Servicio de división (Puerto 5004)
- Monitoring Dashboard: Dashboard de métricas (Puerto 5005)

## Estructura de Carpetas
```
calculator-app/
├── gui/                          # Interfaz web principal
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── addition/                     # Servicio de suma
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── subtraction/                  # Servicio de resta
├── multiplication/               # Servicio de multiplicación
├── division/                     # Servicio de división
├── simulation/                   # Simulador de carga
│   ├── load_test.py
│   └── requirements.txt
├── visualization/                # Dashboard de monitoreo
│   └── realtime_dashboard.py
├── kubernetes/                   # Configuraciones de Kubernetes
│   ├── gui-deployment.yaml
│   ├── addition-deployment.yaml
│   ├── subtraction-deployment.yaml
│   ├── multiplication-deployment.yaml
│   └── division-deployment.yaml
└── docker-compose.yml           # Orquestación local
```

# 🚀 Características
## 🔢 Funcionalidades de Calculadora

- Suma: Operaciones de adición

- Resta: Operaciones de sustracción

- Multiplicación: Operaciones de producto

- División: Operaciones de cociente con protección contra división por cero

## 📊 Monitoreo y Métricas

- Dashboard en Tiempo Real: Visualización de métricas

- Requests por Segundo: Monitoreo de carga

- Tiempos de Respuesta: Latencia de servicios

- Tasa de Errores: Porcentaje de errores

- Distribución de Operaciones: Uso de cada servicio

- Estado de Salud: Monitoreo de disponibilidad

## 🧪 Simulación de Carga

- Pruebas de Estrés: Simulación de múltiples usuarios

- Distribución Realista: Patrones de uso naturales

- Métricas de Rendimiento: Estadísticas detalladas

# 🛠️ Instalación y Configuración
## Prerrequisitos

- Docker y Docker Compose

- Kubernetes (Minikube para desarrollo local)

- Python 3.9+

- Git

## 1. Clonar el Repositorio
```
git clone <repository-url>
cd calculator-app
```
## 2. Configuración con Docker Compose (Desarrollo)
```
# Construir y levantar todos los servicios
docker-compose up --build

# Acceder a la aplicación
# Calculadora: http://localhost:5000
# Dashboard: http://localhost:5005
```
## 3. Configuración con Kubernetes
```
# Iniciar Minikube (si se usa localmente)
minikube start

# Construir imágenes Docker
docker build -t calculator-gui:latest ./gui
docker build -t addition-service:latest ./addition
docker build -t subtraction-service:latest ./subtraction
docker build -t multiplication-service:latest ./multiplication
docker build -t division-service:latest ./division

# Desplegar en Kubernetes
kubectl apply -f kubernetes/

# Verificar despliegue
kubectl get deployments
kubectl get services

# Acceder a la aplicación
minikube service gui-service --url
```
# 📈 Uso y Demostración
## 1. Calculadora Principal

Accede a la interfaz web en http://localhost:5000:

- Ingresa dos números

- Selecciona la operación

- Haz clic en "Calculate"

- Observa el resultado

## 2. Dashboard de Métricas

Accede al dashboard en http://localhost:5005 para ver:

- Métricas en tiempo real

- Distribución de operaciones

- Estado de salud de servicios

- Rendimiento del sistema

## 3. Simulación de Carga
```
cd simulation
pip install -r requirements.txt

# Ejecutar simulación completa
python load_test.py

# Simulaciones individuales
python load_test.py --users 5 --operations 20
```
## 4. Escalado de Servicios

```
# Escalar servicios individualmente
kubectl scale deployment/addition-service --replicas=3
kubectl scale deployment/subtraction-service --replicas=3

# Ver estado de los pods
kubectl get pods