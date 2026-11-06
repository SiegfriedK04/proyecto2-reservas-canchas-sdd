# Sistema de Reservas de Canchas

Proyecto 2 de Tópicos Especiales II. El equipo desarrollará un sistema especializado para consultar disponibilidad y reservar canchas aplicando primero Desarrollo Orientado por Resultados (ODD) y luego Desarrollo Orientado por Especificaciones (SDD).

## Resultado buscado

Permitir que una persona encuentre un horario disponible y complete una reserva sin depender de mensajes manuales, evitando cruces de horario y manteniendo información suficiente para que el administrador controle la operación.

## Estado actual

- Fase activa: descubrimiento ODD y preparación del repositorio.
- Escenario inicial: reservas de canchas deportivas.
- Hipótesis principales documentadas en `specs/outcomes.md`.
- Implementación funcional pendiente hasta aprobar resultados, reglas y criterios de aceptación.

## Equipo y primer ciclo

| Integrante | Responsabilidad inicial |
|---|---|
| Gabriel Rodríguez | Product / Spec Lead y propietario del repositorio |
| Carlos Jaén | Architecture / Development Lead |
| David Ortega | Se incorporará en un ciclo posterior |

Los roles de Gabriel y Carlos se alternarán en cada ciclo. La incorporación de David no detiene las etapas iniciales.

## Forma de trabajo

1. Definir el problema y el resultado esperado mediante ODD.
2. Convertir los resultados aprobados en especificaciones y criterios comprobables.
3. Crear Issues asociados con requisitos concretos.
4. Trabajar en ramas independientes.
5. Revisar los cambios mediante Pull Requests.
6. Ejecutar pruebas automatizadas antes de integrar.
7. Mantener trazabilidad desde la solicitud hasta el resultado.

## Estructura

```text
.
├── specs/
│   ├── outcomes.md
│   ├── requirements.md
│   ├── business-rules.md
│   ├── architecture.md
│   ├── data-model.md
│   ├── api.md
│   ├── acceptance-criteria.md
│   ├── user-stories.md
│   ├── traceability.md
│   └── implementation-plan.md
├── docs/
│   ├── ai-log.md
│   ├── decisions.md
│   ├── roles.md
│   ├── testing.md
│   ├── change-history.md
│   └── issues/
├── src/
└── tests/
```

## Tecnologías propuestas

- Python 3.12
- Django 5.2
- HTML, CSS y JavaScript
- SQLite para desarrollo local
- Django TestCase para pruebas
- GitHub Actions para integración continua

La decisión y sus límites se documentan en `specs/architecture.md`.

## Referencia de proceso

El flujo de Issues, ramas, Pull Requests y pruebas toma como guía el Proyecto 1 del equipo. El código y las especificaciones de este repositorio se desarrollarán de forma independiente para responder al nuevo recorrido ODD y SDD.

