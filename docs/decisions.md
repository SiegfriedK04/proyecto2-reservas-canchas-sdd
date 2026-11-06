# Registro de decisiones

## DEC-001 - Dominio del proyecto

- **Decisión:** desarrollar un sistema de reservas de canchas deportivas.
- **Razón:** el dominio permite demostrar disponibilidad, conflictos, validaciones, administración y cambios de especificación.
- **Consecuencia:** el alcance inicial no incluye pagos ni múltiples sucursales.

## DEC-002 - Relación con el Proyecto 1

- **Decisión:** reutilizar el aprendizaje y el flujo de GitHub, pero crear especificaciones e implementación independientes.
- **Razón:** el Proyecto 2 evalúa el recorrido ODD y SDD, no la repetición del producto anterior.
- **Consecuencia:** cualquier código reutilizado posteriormente deberá identificarse y justificarse.

## DEC-003 - Stack inicial

- **Decisión:** Python y Django con SQLite para desarrollo local.
- **Razón:** el equipo ya conoce las herramientas y puede concentrarse en resultados, reglas y pruebas.
- **Consecuencia:** PostgreSQL se evaluará antes de un despliegue compartido con concurrencia real.

## DEC-004 - Propiedad y colaboración

- **Decisión:** Gabriel será propietario y líder inicial del repositorio; Carlos participará como colaborador y los roles rotarán por ciclo.
- **Razón:** mantiene continuidad con el Proyecto 1 y permite evidencia individual mediante ramas, commits y revisiones.
- **Consecuencia:** David se incorporará cuando su acceso y bloque de trabajo estén definidos.

