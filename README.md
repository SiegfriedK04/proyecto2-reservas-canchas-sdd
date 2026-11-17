# 📅 CourtFlow - Reservas de canchas

<p align="center">
  Aplicación web para descubrir disponibilidad real, reservar canchas y administrar horarios desde un calendario accesible.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/Django-5.2.4-092E20?logo=django&logoColor=white" alt="Django 5.2.4" />
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Tests-58%20passing-success" alt="58 pruebas aprobadas" />
  <a href="https://github.com/SiegfriedK04/proyecto2-reservas-canchas-sdd/actions/workflows/tests.yml">
    <img src="https://github.com/SiegfriedK04/proyecto2-reservas-canchas-sdd/actions/workflows/tests.yml/badge.svg" alt="Pruebas Django" />
  </a>
</p>

---

## 🚀 Descripción

**CourtFlow** resuelve los cruces y demoras propios de coordinar canchas por mensajes. Un visitante puede explorar las canchas activas, consultar un calendario mensual con horarios disponibles y ocupados, crear una cuenta y confirmar una reserva. El cliente también dispone de una agenda organizada con próximas reservas, historial y cancelaciones controladas.

El proyecto documenta el recorrido completo **ODD → SDD → código → pruebas → resultado al usuario**. Las historias, requisitos, reglas, criterios, Issues y Pull Requests están enlazados mediante una matriz de trazabilidad.

Repositorio: [github.com/SiegfriedK04/proyecto2-reservas-canchas-sdd](https://github.com/SiegfriedK04/proyecto2-reservas-canchas-sdd)

---

## ✨ Funcionalidades principales

### Experiencia del cliente

- 🏟️ **Catálogo de canchas activas** con descripción, ubicación y horario operativo.
- ⚡ **Próximo horario libre real** calculado entre todas las canchas activas.
- 📅 **Calendario mensual interactivo** con navegación entre meses y fecha preseleccionable.
- 🟢 **Horarios disponibles y ocupados** diferenciados sin exponer datos privados.
- ✅ **Confirmación transaccional** de reservas desde un resumen de fecha, hora y duración.
- ⛔ **Prevención de doble reserva**, solapamientos y reservas durante bloqueos.
- 🔄 **Alternativas cercanas** cuando el horario solicitado deja de estar disponible.
- 👤 **Registro, autenticación y agenda privada** por cliente.
- 🔔 **Recordatorio de la próxima reserva**, próximas reservas ordenadas e historial separado.
- 🧾 **Cancelaciones auditadas** con un mínimo de dos horas de anticipación.
- 📱 **Diseño adaptable** con navegación móvil, foco visible y soporte para teclado.
- 👨‍💼 **Panel Django Admin** para canchas, reservas, bloqueos y auditoría.

---

## 🧭 ODD y SDD

El desarrollo comenzó por el resultado esperado, no por las pantallas:

> Reducir conflictos de horario y permitir que el cliente encuentre y confirme una cancha disponible sin depender de mensajes manuales.

La documentación principal se encuentra en:

| Etapa | Evidencia |
|---|---|
| ODD | [`specs/outcomes.md`](specs/outcomes.md) |
| Requisitos | [`specs/requirements.md`](specs/requirements.md) |
| Reglas | [`specs/business-rules.md`](specs/business-rules.md) |
| Historias HU-01 a HU-12 | [`specs/user-stories.md`](specs/user-stories.md) |
| Criterios de aceptación | [`specs/acceptance-criteria.md`](specs/acceptance-criteria.md) |
| Plan | [`specs/implementation-plan.md`](specs/implementation-plan.md) |
| Trazabilidad | [`specs/traceability.md`](specs/traceability.md) |

El cambio inesperado solicitado durante el desarrollo añadió una ventana mínima de dos horas para cancelar. Su recorrido desde la especificación y la prueba inicialmente fallida hasta el resultado aprobado está registrado en [`docs/change-history.md`](docs/change-history.md).

---

## 🧰 Tecnologías utilizadas

| Área | Tecnología |
|---|---|
| Backend | Python 3.12 y Django 5.2.4 |
| Frontend | Plantillas Django, HTML5, CSS3 y JavaScript |
| Diseño | Glassmorphism y paleta inspirada en iOS |
| Iconografía | Lucide |
| Base de datos | SQLite para desarrollo local |
| Autenticación | Usuarios, sesiones y validadores de Django |
| Pruebas | Django TestCase |
| Integración continua | GitHub Actions |

La decisión tecnológica, sus límites y la alternativa para un despliegue concurrente se documentan en [`specs/architecture.md`](specs/architecture.md).

---

## 📦 Requisitos previos

- [Python 3.12](https://www.python.org/downloads/) o una versión compatible con Django 5.2.
- `pip`, incluido normalmente con Python.
- Git, si deseas clonar el repositorio.

SQLite se incluye con Python y no requiere una instalación independiente.

---

## ⚡ Inicio rápido en Windows

1. Clona o descarga el repositorio.
2. Abre la carpeta del proyecto.
3. Haz doble clic en `iniciar_app.cmd`.
4. Visita [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

El iniciador crea `.venv` cuando hace falta, instala dependencias, aplica migraciones, prepara los datos de demostración e inicia el servidor.

---

## ⚙️ Instalación manual

### 1. Clonar el repositorio

```bash
git clone https://github.com/SiegfriedK04/proyecto2-reservas-canchas-sdd.git
cd proyecto2-reservas-canchas-sdd
```

### 2. Crear y activar el entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En CMD utiliza `.venv\Scripts\activate.bat`. En Linux o macOS utiliza `source .venv/bin/activate`.

### 3. Instalar y preparar la aplicación

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py crear_datos_demo
```

### 4. Iniciar el servidor

```powershell
python manage.py runserver
```

---

## 🔐 Configuración del entorno

`.env.example` documenta las variables admitidas. Django las lee desde el entorno del proceso:

```env
DJANGO_SECRET_KEY=replace-this-outside-local-development
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

| Variable | Descripción |
|---|---|
| `DJANGO_SECRET_KEY` | Clave criptográfica; debe reemplazarse fuera del entorno local. |
| `DJANGO_DEBUG` | Activa o desactiva el modo de depuración. |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos separados por comas. |

---

## 🧪 Datos de demostración

```powershell
python manage.py crear_datos_demo
```

El comando es repetible y prepara tres canchas, reservas variadas, un bloqueo operativo y dos cuentas:

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador | `admin_user` | `admin1234` |
| Cliente | `demo_user` | `demo1234` |

> Estas credenciales son exclusivamente para desarrollo y demostración local.

---

## 🌍 Rutas principales

| Ruta | Acceso | Descripción |
|---|---|---|
| `/` | Público | Catálogo y próximo horario libre. |
| `/registro/` | Público | Creación de una cuenta. |
| `/login/` | Público | Inicio de sesión. |
| `/canchas/<id>/reservar/` | Público / autenticado | Calendario y horarios; confirmar requiere sesión. |
| `/mis-reservas/` | Cliente | Próxima reserva, agenda, historial y cancelaciones. |
| `/admin/` | Administrador | Gestión operativa y auditoría. |

El calendario acepta `?fecha=AAAA-MM-DD` para abrir una fecha futura específica.

---

## 🔌 API interna

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/canchas/<court_id>/disponibilidad/?date=AAAA-MM-DD` | Devuelve horarios disponibles y ocupados. |
| `POST` | `/api/reservas/` | Confirma una reserva autenticada. |
| `POST` | `/mis-reservas/<booking_id>/cancelar/` | Cancela una reserva propia elegible. |

Las operaciones de escritura validan sesión, CSRF, permisos, horario operativo, conflictos y bloqueos en el servidor.

---

## 📁 Estructura del proyecto

```text
proyecto2-reservas-canchas-sdd/
├── courtflow/                   # Configuración de Django
├── reservations/               # Modelos, servicios, vistas, administración y pruebas
│   ├── management/commands/    # Datos de demostración
│   ├── migrations/             # Esquema de base de datos
│   └── tests/                  # Suite automatizada
├── templates/                  # Interfaz HTML
├── static/                     # CSS y JavaScript del calendario
├── specs/                      # ODD, SDD, arquitectura y trazabilidad
├── docs/                       # Decisiones, pruebas, historial, roles y registro de IA
├── .github/workflows/tests.yml # Integración continua
├── .env.example
├── iniciar_app.cmd
├── manage.py
├── requirements.txt
└── README.md
```

La organización de Django reemplaza las carpetas genéricas `src/` y `tests/` de la estructura recomendada: el código y las pruebas residen dentro de `reservations/`.

---

## ⚙️ Comandos disponibles

| Comando | Descripción |
|---|---|
| `python manage.py runserver` | Inicia el servidor de desarrollo. |
| `python manage.py migrate` | Aplica las migraciones pendientes. |
| `python manage.py crear_datos_demo` | Prepara usuarios, canchas y reservas demo. |
| `python manage.py createsuperuser` | Crea otra cuenta administrativa. |
| `python manage.py check` | Comprueba la configuración de Django. |
| `python manage.py makemigrations --check --dry-run` | Verifica que no falten migraciones. |
| `python manage.py test` | Ejecuta toda la suite automatizada. |

---

## 🧪 Pruebas automatizadas

La suite contiene **58 pruebas** que cubren servicios, modelos, vistas, API y criterios de aceptación.

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

| Grupo | Casos principales |
|---|---|
| Reservas | Creación, horarios, conflictos, intervalos y atomicidad. |
| Disponibilidad | Reservas, bloqueos, horarios ocupados, privacidad y rendimiento de consultas. |
| Usuarios | Registro, correo único, autenticación y permisos. |
| Cancelaciones | Propiedad, ventana de dos horas, excepción administrativa y auditoría. |
| Agenda | Próxima reserva, orden cronológico, historial y estados finalizados. |
| Accesibilidad | Navegación móvil, enlace de salto, foco y atributos ARIA. |
| Portada | Próximo horario real, canchas inactivas y fechas válidas. |
| Datos demo | Idempotencia, credenciales y panel administrativo. |

GitHub Actions ejecuta las comprobaciones y pruebas en cada Pull Request y actualización de `main`.

---

## 🛡️ Seguridad e integridad

- Protección CSRF en operaciones de escritura.
- Contraseñas gestionadas y validadas por Django.
- Correo electrónico normalizado y sin duplicados.
- Permisos y propiedad verificados antes de cancelar.
- Reglas críticas validadas en el servidor.
- Creación y cancelación dentro de transacciones.
- Horarios ocupados sin identidad del cliente ni motivo del bloqueo.
- Auditoría persistente de creaciones y cancelaciones.
- SQLite limitado a desarrollo local; para concurrencia compartida se recomienda PostgreSQL.

---

## 🔄 Flujo de trabajo y evidencias

El repositorio demuestra Issues, ramas, commits identificables, Pull Requests, revisiones cruzadas y CI. Los principales registros son:

- [`docs/ai-log.md`](docs/ai-log.md): actividad, herramienta, solicitud, resultado y decisión.
- [`docs/change-history.md`](docs/change-history.md): evolución y cambio inesperado de especificación.
- [`docs/testing.md`](docs/testing.md): estrategia, casos y resultados.
- [`docs/roles.md`](docs/roles.md): rotación de Product/Spec, Architecture/Development y QA/DevOps.
- [`docs/compliance-checklist.md`](docs/compliance-checklist.md): cumplimiento de las restricciones del Proyecto 2.
- [`docs/presentation-guide.md`](docs/presentation-guide.md): recorrido recomendado para la exposición.

---

## ⚠️ Consideraciones

- El servidor incorporado es para desarrollo, no para producción.
- Las credenciales demo y `DJANGO_SECRET_KEY` deben cambiarse en un entorno compartido.
- Lucide y la tipografía Inter se cargan desde servicios externos; sin Internet la aplicación conserva su funcionalidad, pero puede utilizar tipografía de respaldo y omitir iconos.
- La búsqueda del próximo horario consulta una ventana de siete días.

---

## 👥 Equipo

- **Gabriel Rodríguez**
- **Carlos Jaén**
- **David Ortega**

Los roles se rotaron por ciclos y cada integrante dejó evidencia mediante Issues, ramas, commits y Pull Requests.

Proyecto académico de **Tópicos Especiales II**.
