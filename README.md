# GreenDrive

Plataforma web para la gestión integral de flotas de micromovilidad eléctrica: permite a las personas usuarias localizar vehículos disponibles en un mapa, reservarlos y finalizar su uso, mientras que el personal administrador monitoriza el estado de cada vehículo en tiempo real.

## Índice

- [Resumen](#-resumen)
- [Funcionalidades clave](#-funcionalidades-clave)
- [Arquitectura](#-arquitectura)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Stack tecnológico](#-stack-tecnológico)
- [Configuración y variables de entorno](#-configuración-y-variables-de-entorno)
- [Instalación](#-instalación)
- [Puesta en marcha](#-puesta-en-marcha)
- [Flujos funcionales](#-flujos-funcionales)
- [API y endpoints](#-api-y-endpoints)
- [Datos en MongoDB](#-datos-en-mongodb)
- [Tareas en segundo plano](#-tareas-en-segundo-plano)
- [Documentación adicional](#-documentación-adicional)
- [Próximos pasos sugeridos](#-próximos-pasos-sugeridos)

## 📖 Resumen

GreenDrive es un prototipo completo de *car sharing* eléctrico construido sobre Flask. Se compone de tres grandes capas:

1. **Presentación**: plantillas Jinja, Bootstrap y JavaScript para la experiencia web (páginas de login, listado de vehículos, reserva activa y panel de administración).
2. **Dominio**: blueprints especializados (`auth`, `vehiculo`, `reserve`, `map`, `chatbot`, `admin`) que encapsulan la lógica de negocio.
3. **Persistencia**: capa DAO sobre MongoDB Atlas que centraliza el acceso a las colecciones de usuarios, vehículos y reservas.

El sistema incorpora mapas de Google, un asistente de emergencias basado en reconocimiento de voz, actualizaciones periódicas del estado de la batería y un dashboard administrativo con telemetría detallada.

## ✨ Funcionalidades clave

- **Autenticación y registro** con hashing de contraseñas y gestión de sesiones (roles *user* y *admin*).
- **Catálogo de vehículos** con tarjetas animadas, disponibilidad filtrada y reserva en un clic.
- **Mapa interactivo** con geovallas y marcadores personalizados alimentados desde `/map/data`.
- **Gestión de reservas**: control de reservas activas, cronómetro en vivo, cálculo del coste y liberación del vehículo.
- **Panel administrativo** con detalles técnicos (batería, neumáticos, conectividad, errores) y polling para datos actualizados.
- **Chat de emergencia** que usa *Web Speech API* para transcribir peticiones y clasificar el tipo de incidente vía endpoint Flask.
- **Actualizaciones automáticas de telemetría** mediante `APScheduler`, simulando carga/descarga de baterías y velocidad.

## 🧱 Arquitectura

```mermaid
flowchart LR
    subgraph Presentación
        Templates[Plantillas Jinja]
        Static[JS + CSS + Web Speech API]
    end
    subgraph Dominio (Flask)
        AuthBP[Blueprint auth]
        VehicleBP[Blueprint vehiculo]
        ReserveBP[Blueprint reserve]
        MapBP[Blueprint map]
        ChatbotBP[Blueprint chatbot]
        AdminBP[Blueprint admin]
    end
    subgraph Persistencia
        MongoDB[MongoDB Agent]
        DAOs[DAOs: User/Vehiculo/Reservas]
    end

    Templates -- HTTP --> AuthBP
    Templates -- HTTP --> VehicleBP
    Templates -- HTTP --> ReserveBP
    Templates -- HTTP --> MapBP
    Templates -- HTTP --> ChatbotBP
    Templates -- HTTP --> AdminBP

    AuthBP --> DAOs
    VehicleBP --> DAOs
    ReserveBP --> DAOs
    MapBP --> DAOs
    ChatbotBP -.-> |Clasificación| lógicaChat[Diccionario de emergencias]
    DAOs --> MongoDB

    Static -. fetch .-> MapBP
    Static -. fetch .-> VehicleBP
    Static -. fetch .-> ChatbotBP
```

### Rutas y responsabilidades

| Blueprint | Prefijo | Responsabilidad principal |
|-----------|---------|---------------------------|
| `auth`    | `/`     | Registro, login, logout, listado de usuarios y bloqueo. |
| `vehiculo`| `/vehiculos` | Catálogo, reservas, control de estado, bloqueo y simulaciones. |
| `reserve` | `/reserve` | Gestión de reserva activa y cierre con cálculo de coste. |
| `map`     | `/map`  | Páginas y API JSON para Google Maps. |
| `chatbot` | `/chatbot` | Procesamiento de transcripciones de emergencia. |
| `admin`   | `/admin` | Dashboard de monitoreo para personal administrador. |

## 🗂️ Estructura del proyecto

```
GreenDrive/
├── Dominio/
│   ├── server.py               # Bootstrap del servidor Flask
│   ├── auth.py                 # Blueprint de autenticación
│   ├── vehicle.py              # Blueprint con lógica de vehículos y reservas
│   ├── reserve.py              # Gestión de reservas activas
│   ├── map.py                  # Endpoints del mapa
│   ├── chatbot.py              # Clasificador de emergencias
│   ├── admin.py                # Panel de administración
│   ├── utils.py                # Filtros utilitarios para Jinja
│   └── Entidades/
│       └── user.py             # Modelo base de usuario
├── Persistencia/
│   ├── AgenteBD.py             # Conexión centralizada a MongoDB Atlas
│   └── DAOS/
│       ├── UserDAO.py
│       ├── VehiculoDAO.py
│       └── ReservasDAO.py
├── Presentacion/
│   ├── templates/              # Plantillas Jinja (login, mapa, listados, admin)
│   └── static/                 # CSS, JS y recursos gráficos
├── doc/                        # Memorias DGSI (fases 1-3)
├── requirements.txt
├── setup&run.bat / setup&run.sh
└── README.md
```

## 🛠️ Stack tecnológico

- **Backend**: Python 3.12, Flask 3, Blueprints, Jinja2.
- **Persistencia**: MongoDB Atlas, PyMongo 4.
- **Frontend**: HTML5, CSS3, Bootstrap 4, JavaScript vanilla, Google Maps JS API, Web Speech API.
- **Jobs**: APScheduler para tareas recurrentes.
- **Utilidades**: python-dotenv para variables de entorno, Werkzeug para hashing de contraseñas.

## ⚙️ Configuración y variables de entorno

Crea un fichero `.env` en la raíz del proyecto con las siguientes claves:

| Variable | Descripción |
|----------|-------------|
| `FLASK_SECRET_KEY` | Clave secreta usada por Flask para sesiones y protección CSRF. |
| `BBDD_PASSWD` | Contraseña del usuario `deliveringsolutionssl` en el clúster MongoDB Atlas proporcionado. |
| `GOOGLE_API_KEY` | API key con acceso a Google Maps JavaScript API. |

> 💡 Mantén estos valores fuera del control de versiones. Puedes partir de este ejemplo:

```env
FLASK_SECRET_KEY=super-secreto
BBDD_PASSWD=tu_password_de_mongo
GOOGLE_API_KEY=tu_api_key_de_google
```

## 🧰 Instalación

### Prerrequisitos

- Python 3.12 (o versión compatible con los wheels incluidos).
- Acceso a internet para instalar dependencias y conectar con MongoDB Atlas.
- API key válida de Google Maps.

### Instalación rápida (Windows PowerShell)

```powershell
python -m venv myenv
myenv\Scripts\Activate.ps1
pip install -r requirements.txt
notepad .env  # crea el fichero y pega las variables del ejemplo anterior
python Dominio\server.py
```

### Instalación alternativa (Linux / macOS)

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
export FLASK_SECRET_KEY=...
export BBDD_PASSWD=...
export GOOGLE_API_KEY=...
python3 Dominio/server.py
```

También puedes usar los scripts `setup&run.bat` o `setup&run.sh`, que automatizan la creación del entorno virtual, la instalación de dependencias y el arranque de Flask.

## ▶️ Puesta en marcha

1. Arranca el servidor Flask (`python Dominio/server.py`).
2. Abre `http://localhost:5000/` en tu navegador.
3. Registra un nuevo usuario o accede con uno existente.
4. Para acceder al panel de administración, marca el usuario como `role: "admin"` en la colección `usuarios`.

## 🚦 Flujos funcionales

### Usuario final

1. **Login / Registro** desde `loginRegister.html`.
2. **Listado de vehículos** (`/vehiculos`):
   - Mapa centrado en Talavera con geovalla.
   - Tarjetas animadas con datos de batería, coste y botón de reserva.
3. **Reserva activa** (`/reserve`):
   - Cronómetro en tiempo real.
   - Posibilidad de finalizar la reserva con cálculo de precio.
4. **Asistencia de emergencia**: widget emergente que transcribe voz y despacha la ayuda adecuada.

### Administrador

1. Inicia sesión con un usuario que tenga `role = "admin"`.
2. Accede a `/admin/dashboard` para ver la tabla de vehículos.
3. Al pulsar una fila, se abre un modal con telemetría técnica, neumáticos, conectividad y errores.
4. El panel se refresca automáticamente cada minuto vía *polling*.

## 🔌 API y endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET    | `/` | Redirección al formulario de login. |
| POST   | `/login` | Autenticación de usuarios. |
| POST   | `/register` | Alta de nuevos usuarios. |
| GET    | `/vehiculos` | Listado web de vehículos disponibles. |
| GET    | `/vehiculos/json` | Catálogo completo en JSON (usado por admin). |
| GET    | `/vehiculos/detalles/<id>` | Telemetría detallada de un vehículo. |
| PUT    | `/vehiculos/<id>/reservar` | Reserva directa por ID (API). |
| POST   | `/vehiculos/reservar` | Reserva a partir de matrícula (usado por frontend). |
| POST   | `/vehiculos/<id>/bloquear` | Bloqueo/desbloqueo remoto. |
| POST   | `/vehiculos/<id>/pinchazo` | Reportar pinchazo en un neumático concreto. |
| PUT    | `/vehiculos/<id>/actualizar_estado` | Cambiar estado general del vehículo. |
| GET    | `/reserve/` | Vista de reserva activa. |
| POST   | `/reserve/finish` | Finaliza la reserva y calcula importe. |
| GET    | `/map/` | Página con mapa interactivo. |
| GET    | `/map/data` | JSON con posiciones e iconos de los vehículos. |
| GET    | `/api/vehicle_status` | Niveles de batería para *polling* periódico. |
| POST   | `/chatbot/transcripcion` | Clasifica mensajes de emergencia. |
| GET    | `/auth/users` | Devuelve la lista de usuarios (uso interno). |
| GET    | `/auth/logout` | Cierra la sesión actual. |
| GET    | `/admin/admin/dashboard` | Panel de monitoreo para personas administradoras. |

> ℹ️ Los endpoints que modifican datos requieren que el usuario esté autenticado y que el frontend provea el `id_usuario` en la carga útil.

## 🗄️ Datos en MongoDB

Colecciones utilizadas:

- **`usuarios`**: `{ name, email, pass, role, blocked }`.
- **`vehiculos`**: datos generales + `bateria`, `ubicacion`, `neumaticos`, `conectividad`, `motor`, `bloqueo`.
- **`reservas`**: `{ id_usuario, id_vehiculo, fecha_inicio, fecha_fin, estado }`.

Asegúrate de contar con datos de muestra en `vehiculos` para que el mapa y los listados se rendericen correctamente.

## ⏱️ Tareas en segundo plano

Se utiliza `BackgroundScheduler` de APScheduler para ejecutar `actualizar_bateria_periodica()` cada minuto. Esta tarea:

- Simula la recarga de baterías en vehículos disponibles (+10%).
- Simula el consumo en vehículos ocupados (-5%) y actualiza la velocidad con un valor aleatorio.
- Guarda los cambios en MongoDB para que el frontend refleje los nuevos valores a través de *polling*.

## 📚 Documentación adicional

En la carpeta `doc/` encontrarás las memorias DGSI de las distintas fases del proyecto (`DGSI_P1_GrupoC.pdf`, `DGSI_P2_GrupoC.pdf`, `DGSI_P3_GrupoC.pdf`). Amplían los requisitos, casos de uso y la justificación técnica.

## 🚀 Próximos pasos sugeridos

- Añadir pruebas automatizadas (unitarias e integración) para la lógica crítica.
- Incorporar control de acceso a nivel de endpoint (decoradores o middleware).
- Gestionar inventario y telemetría en tiempo real mediante websockets en lugar de *polling*.
- Añadir despliegue automatizado (Docker + CI/CD) y scripts de `seed` de datos.
- Proveer una plantilla `.env.example` y fixtures para poblar colecciones con datos de prueba.

---
