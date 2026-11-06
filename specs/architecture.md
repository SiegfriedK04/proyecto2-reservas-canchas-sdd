# Arquitectura

## Decisión tecnológica inicial

Se propone una aplicación web monolítica con Django porque el equipo ya conoce su modelo de desarrollo, autenticación, migraciones, panel administrativo y sistema de pruebas. La decisión reduce el tiempo invertido en configuración y permite concentrar la evaluación en ODD, SDD, trazabilidad y reglas de reserva.

## Stack

| Área | Tecnología |
|---|---|
| Lenguaje | Python 3.12 |
| Framework | Django 5.2 |
| Interfaz | Plantillas Django, HTML, CSS y JavaScript |
| Base de datos local | SQLite |
| Base de datos de despliegue | PostgreSQL si se habilita un entorno compartido |
| Pruebas | Django TestCase |
| Integración continua | GitHub Actions |

## Componentes previstos

- `accounts`: registro, autenticación y perfil básico.
- `venues`: canchas, horarios de operación y bloqueos.
- `bookings`: disponibilidad, creación, consulta y cancelación.
- `audit`: eventos relevantes de reservas y administración.

## Límites

- Las reglas críticas pertenecen al servidor y no dependen del JavaScript del navegador.
- La interfaz consume servicios internos del mismo proyecto; no se propone microservicios para el alcance académico.
- SQLite se utiliza únicamente para desarrollo local. Si existe concurrencia compartida se evaluará PostgreSQL.
- No se copiará la implementación del Proyecto 1. Se reutiliza el aprendizaje del equipo y el patrón de trabajo en GitHub.

## Seguridad básica

- Autenticación de Django.
- Protección CSRF.
- Validación de propiedad y permisos.
- Transacciones en la creación y cancelación.
- Mensajes de conflicto sin datos privados.

