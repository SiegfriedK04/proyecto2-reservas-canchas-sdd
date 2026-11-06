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

## Flujo de creación de una reserva

1. La vista valida autenticación y formato de los datos.
2. Un servicio de dominio abre una transacción.
3. El servicio obtiene la cancha y comprueba horario operativo.
4. Se consultan reservas confirmadas y bloqueos que intersecten el intervalo.
5. Si existe conflicto, se devuelve un rechazo estable sin modificar datos.
6. Si no existe conflicto, se crea la reserva y su evento de auditoría.

La comprobación y la escritura deben pertenecer a la misma operación. La interfaz no puede decidir por sí sola que un horario continúa disponible.

## Concurrencia

SQLite es suficiente para la demostración local, pero no representa el comportamiento final bajo múltiples solicitudes simultáneas. Para un entorno compartido se utilizará PostgreSQL y se revisará una estrategia de bloqueo o restricción que evite que dos transacciones confirmen el mismo intervalo. Las pruebas del proyecto cubrirán el resultado observable aunque el mecanismo cambie por motor de base de datos.

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

