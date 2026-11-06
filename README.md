# CourtFlow — Sistema de reservas de canchas

CourtFlow permite consultar canchas, revisar su disponibilidad en un calendario mensual y confirmar una reserva sin depender de mensajes manuales. El proyecto aplica Desarrollo Orientado por Resultados (ODD) y Desarrollo Orientado por Especificaciones (SDD), con trazabilidad entre historias, reglas, pruebas, Issues y Pull Requests.

## Funciones principales

- Catálogo de canchas activas con ubicación y horario operativo.
- Registro, inicio de sesión y gestión segura de usuarios.
- Calendario mensual interactivo con horarios disponibles.
- Confirmación transaccional de reservas sin solapamientos.
- Mensajes claros y alternativas cuando un horario ya no está disponible.
- Consulta y cancelación de reservas propias.
- Administración de canchas, bloqueos y eventos de auditoría.
- Interfaz adaptable con glassmorphism y una paleta inspirada en iOS.

## Inicio rápido en Windows

1. Instala Python 3.12 o una versión compatible.
2. Abre la carpeta del proyecto.
3. Ejecuta `iniciar_app.cmd`.
4. Visita `http://127.0.0.1:8000/`.

El iniciador crea el entorno virtual, instala dependencias, aplica migraciones y prepara datos de demostración cuando sea necesario.

### Cuentas de demostración

| Perfil | Usuario | Contraseña |
|---|---|---|
| Administrador | `admin_user` | `admin1234` |
| Cliente | `demo_user` | `demo1234` |

La administración está disponible en `http://127.0.0.1:8000/admin/`.

## Ejecución manual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py crear_datos_demo
python manage.py runserver
```

## Pruebas

```powershell
python manage.py test
python manage.py check
```

La suite cubre reglas de horario, conflictos, bloqueos, permisos, registro, calendario, API, cancelaciones y auditoría.

## Historias de usuario

El backlog funcional está numerado de **HU-01** a **HU-09** en [`specs/user-stories.md`](specs/user-stories.md). Cada historia incluye criterios verificables y su relación con requisitos y pruebas.

## Estructura del proyecto

```text
courtflow/                 Configuración de Django
reservations/              Dominio, servicios, vistas, formularios y pruebas
templates/                 Interfaz HTML
static/                    Estilos y comportamiento del calendario
specs/                     Outcomes, requisitos, reglas, historias y trazabilidad
docs/                      Decisiones, roles, pruebas e historial de cambios
iniciar_app.cmd            Inicio simplificado en Windows
```

## Equipo

- Gabriel Rodríguez — liderazgo del repositorio, producto y desarrollo.
- Carlos Jaén — arquitectura, desarrollo y revisión.
- David Ortega — mejoras complementarias del producto en el ciclo final.

Los roles de especificación, implementación y revisión se alternan por ciclo para mantener revisión cruzada.
