# Eventia Core API

Sistema de gestión de eventos, participantes y asistencia construido con Flask, MySQL y Redis.


# Tabla de Contenidos

- [Introducción](#introducción)
- [Arquitectura](#arquitectura)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución en Local](#ejecución-en-local)
- [Ejecución de Pruebas](#ejecución-de-pruebas)
- [Pipeline CI/CD](#pipeline-cicd)
- [Endpoints de la API](#endpoints-de-la-api)
- [Estructura del Proyecto](#estructura-del-proyecto)

# Introducción

Eventia Core API es un sistema backend que permite gestionar eventos, participantes y registros de asistencia. Implementa reglas de negocio como validación de cupos, prevención de registros duplicados y generación de estadísticas en tiempo real.

# Funcionalidades principales:

- CRUD completo de eventos
- CRUD completo de participantes
- Registro de asistencia con validaciones
- Verificación de capacidad de eventos
- Estadísticas de ocupación en tiempo real
- Sistema de caché con Redis
- Pruebas automatizadas (unitarias, integración, sistema)


# Arquitectura

El proyecto sigue una arquitectura MVC (Modelo-Vista-Controlador)** adaptada para APIs REST:
```
┌─────────────────────────────────────────────┐
│            Cliente (Postman, etc)           │
└──────────────────┬──────────────────────────┘
                   │ HTTP Requests
                   ▼
┌─────────────────────────────────────────────┐
│              Routes (Rutas)                 │
│  - Define endpoints y métodos HTTP          │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│          Controllers (Controladores)        │
│  - Maneja requests HTTP                     │
│  - Valida datos de entrada                  │
│  - Devuelve respuestas JSON                 │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│           Services (Servicios)              │
│  - Lógica de negocio                        │
│  - Validaciones de reglas                   │
│  - Interacción con caché                    │
└──────────────────┬──────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌──────────────┐      ┌──────────────┐
│   Database   │      │    Redis     │
│   (MySQL)    │      │   (Caché)    │
└──────────────┘      └──────────────┘

# Capas de la arquitectura:

1. Rutas (Routes): Define los endpoints de la API
2. Controladores (Controllers): Maneja peticiones HTTP y respuestas
3. Servicios (Services): Contiene la lógica de negocio
4. Modelos (Models): Representa las entidades del dominio
5. Base de Datos: Persistencia de datos
6. Caché: Optimización de consultas frecuentes

# Principios aplicados:

- Separación de responsabilidades: Cada capa tiene un propósito específico
- Desacoplamiento: Las capas se comunican mediante interfaces claras
- Inyección de dependencias: Facilita las pruebas y mantenimiento
- Single Responsibility Principle: Cada clase/módulo tiene una única responsabilidad


#  Tecnologías Utilizadas

# Backend:
- Python 3.11+ - Lenguaje de programación
- Flask 3.0 - Framework web ligero y flexible
- Flask-CORS - Manejo de CORS para APIs

# Base de Datos:
- MySQL 8.0 - Base de datos relacional
- mysql -connector-python - Driver oficial de MySQL para Python

# Caché:
- Redis - Sistema de caché en memoria para optimizar consultas

# Testing: - pytest - Framework de pruebas
- pytest-cov - Medición de cobertura de código

# Seguridad:
- Bandit - Análisis estático de seguridad

# CI/CD:
- GitHub Actions - Integración y despliegue continuo

# Justificación de elección de tecnologías:

| Tecnología | Justificación |
|------------|---------------|
| Flask | Framework ligero, ideal para APIs REST. Fácil de aprender y muy flexible. |
| MySQL | Base de datos robusta y ampliamente adoptada. Excelente para datos relacionales. |
| Redis | Caché en memoria ultra-rápida. Reduce carga en la BD y mejora tiempos de respuesta. |
| pytest | Framework de testing más popular en Python. Sintaxis simple y potente. |
| Docker | Asegura consistencia entre entornos de desarrollo, testing y producción. |


# Requisitos

# Software necesario:

- Python 3.11 o superior
- MySQL 8.0 o superior
- Redis 6.0 o superior
- Git
- pip (gestor de paquetes de Python)

# Para desarrollo local con Laragon:
- Laragon (incluye MySQL y Apache)

# Para desarrollo con Docker:
- Docker Desktop


# Instalación

# 1. Clonar el repositorio:
```bash
git clone https://github.com/jasbleidy2005/eventia-core-api.git
cd eventia-core-api
```

# 2. Crear entorno virtual:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

# 3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

# 4. Configurar variables de entorno:

Copia el archivo de ejemplo:
```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=eventia_db

REDIS_HOST=localhost
REDIS_PORT=6379

FLASK_ENV=development
FLASK_PORT=5000
```

# 5. Crear la base de datos:

Opción A: Con MySQL CLI
```bash
mysql -u root -p < database/schema.sql
```
Opción B: Con phpMyAdmin (Laragon)

1. Ir a `http://localhost/phpmyadmin/`
2. Crear base de datos `eventia_db`
3. Ejecutar el contenido de `database/schema.sql`

# 6. Iniciar Redis:

Con Docker:
```bash
docker run -d --name redis-eventia -p 6379:6379 redis:latest
```

O con Laragon/instalación local:
```bash
redis-server
```

---

#  Ejecución en Local

## 1. Asegurarse de que MySQL y Redis están corriendo
```bash
# Verificar MySQL (con Laragon o servicio local)
mysql -u root -p -e "SELECT 1"

# Verificar Redis
docker ps | grep redis
# O
redis-cli ping
```

# 2. Activar el entorno virtual (si no está activo)
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

# 3. Ejecutar la aplicación:
```bash
python src/app.py
```

La API estará disponible en: `http://localhost:5000`

# 4. Verificar que funciona:
```bash
curl http://localhost:5000/
```

Respuesta esperada:
```json
{
  "status": "OK",
  "message": "Eventia Core API is running"
}
```

---

#  Ejecución de Pruebas

# Ejecutar todas las pruebas:
```bash
pytest
```

# Ejecutar con reporte detallado:
```bash
pytest -v
```

# Ejecutar por tipo:
```bash
# Solo pruebas unitarias
pytest tests/unit/ -v

# Solo pruebas de integración
pytest tests/integration/ -v

# Solo pruebas de sistema
pytest tests/system/ -v
```

# Generar reporte de cobertura:
```bash
pytest --cov=src --cov-report=html
```

El reporte se generará en `htmlcov/index.html`. Ábrelo en el navegador para ver la cobertura detallada.

# Ejecutar análisis de seguridad:
```bash
bandit -r src/
```

---

#  Pipeline CI/CD

El proyecto utiliza **GitHub Actions** para integración continua. El pipeline se ejecuta automáticamente en cada push o pull request.

#Pasos del pipeline:

1. Checkout del código
2. Configuración de Python 3.11
3. Instalación de dependencias
4. Inicio de servicios (MySQL y Redis)
5. Creación de esquema de base de datos
6. Ejecución de pruebas unitarias
7. Ejecución de pruebas de integración
8. Ejecución de pruebas de sistema
9. Análisis estático de seguridad con Bandit
10. Generación de reportes

# Resultado esperado:

Si todos los pasos pasan exitosamente, el pipeline imprime:
```
================================
           OK                
================================
All tests and checks passed!
```

# Ver el estado del pipeline:

1. Ve a tu repositorio en GitHub
2. Click en la pestaña **"Actions"**
3. Verás el historial de ejecuciones

# Archivo de configuración:

El pipeline está definido en: `.github/workflows/ci.yml`

---

#  Endpoints de la API

# Health Check
```
GET /
```

Respuesta:
```json
{
  "status": "OK",
  "message": "Eventia Core API is running"
}
```

---

# Eventos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/events` | Crear evento |
| `GET` | `/api/events` | Listar todos los eventos |
| `GET` | `/api/events/{id}` | Obtener evento por ID |
| `PUT` | `/api/events/{id}` | Actualizar evento |
| `DELETE` | `/api/events/{id}` | Eliminar evento |

Ejemplo - Crear evento:
```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Conferencia Tech 2025",
    "description": "Evento de tecnología",
    "date": "2025-12-15T10:00:00",
    "location": "Auditorio Principal",
    "capacity": 200
  }'
```


#Participantes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/participants` | Crear participante |
| `GET` | `/api/participants` | Listar todos los participantes |
| `GET` | `/api/participants/{id}` | Obtener participante por ID |
| `PUT` | `/api/participants/{id}` | Actualizar participante |
| `DELETE` | `/api/participants/{id}` | Eliminar participante |

Ejemplo - Crear participante:
```bash
curl -X POST http://localhost:5000/api/participants \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "1234567890"
  }'
```


# Asistencia

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/attendance` | Registrar asistencia |
| `GET` | `/api/attendance/event/{id}/participants` | Participantes de un evento |
| `GET` | `/api/attendance/participant/{id}/events` | Eventos de un participante |
| `GET` | `/api/attendance/event/{id}/statistics` | Estadísticas de un evento |
| `DELETE` | `/api/attendance/event/{id}/participant/{pid}` | Cancelar asistencia |

Ejemplo - Registrar asistencia:
```bash
curl -X POST http://localhost:5000/api/attendance \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "participant_id": 1
  }'
```

Ejemplo - Ver estadísticas:
```bash
curl http://localhost:5000/api/attendance/event/1/statistics
```

Respuesta:
```json
{
  "event_id": 1,
  "event_name": "Conferencia Tech 2025",
  "capacity": 200,
  "registered": 150,
  "available": 50,
  "occupancy_percentage": 75.0
}
```

---

#  Estructura del Proyecto
```
eventia-core-api/
│
├── .github/
│   └── workflows/
│       └── ci.yml                 # Pipeline de CI/CD
│
├── src/
│   ├── models/                    # Modelos de dominio
│   │   ├── event.py
│   │   ├── participant.py
│   │   └── attendance.py
│   │
│   ├── services/                  # Lógica de negocio
│   │   ├── event_service.py
│   │   ├── participant_service.py
│   │   └── attendance_service.py
│   │
│   ├── controllers/               # Manejo de HTTP
│   │   ├── event_controller.py
│   │   ├── participant_controller.py
│   │   └── attendance_controller.py
│   │
│   ├── routes/                    # Definición de endpoints
│   │   ├── event_routes.py
│   │   ├── participant_routes.py
│   │   └── attendance_routes.py
│   │
│   ├── database/                  # Configuración de BD
│   │   └── connection.py
│   │
│   ├── cache/                     # Cliente de Redis
│   │   └── redis_client.py
│   │
│   ├── config/                    # Configuraciones
│   │   └── settings.py
│   │
│   └── app.py                     # Aplicación principal
│
├── tests/
│   ├── unit/                      # Pruebas unitarias
│   │   ├── test_event_service.py
│   │   └── test_attendance_service.py
│   │
│   ├── integration/               # Pruebas de integración
│   │   ├── test_event_api.py
│   │   └── test_participant_api.py
│   │
│   ├── system/                    # Pruebas end-to-end
│   │   └── test_full_flow.py
│   │
│   └── conftest.py                # Configuración de pytest
│
├── database/
│   └── schema.sql                 # Esquema de base de datos
│
├── .env.example                   # Ejemplo de variables de entorno
├── .gitignore                     # Archivos ignorados por Git
├── pytest.ini                     # Configuración de pytest
├── requirements.txt               # Dependencias de Python
└── README.md                      # Este archivo
```


# Ejecutar con Docker Compose:
```bash
docker-compose up -d
```

Esto iniciará:
- Backend (Flask)
- MySQL
- Redis

La API estará disponible en `http://localhost:5000`

# Detener los contenedores:
```bash
docker-compose down
```

---

#  Autor

Karen Jasbleidy Lopez Ruiz - klopez2227@cue.edu.co

#  Licencia

Este proyecto fue desarrollado como parte del curso de pruebas.

