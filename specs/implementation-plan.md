# Plan de implementación

## Ciclo 0 - Fundación

- Crear el repositorio bajo la propiedad de Gabriel.
- Incorporar a Carlos como colaborador.
- Registrar resultados ODD, decisiones y roles.
- Crear el backlog inicial y las etiquetas de trabajo.

## Ciclo 1 - Especificaciones y arquitectura

- Aprobar requisitos y reglas de negocio.
- Revisar arquitectura, modelo de datos y contrato de API.
- Convertir criterios de aceptación en pruebas inicialmente fallidas.
- Roles: Gabriel como Product / Spec Lead y Carlos como Architecture / Development Lead.

## Ciclo 2 - Reserva mínima

- Crear proyecto Django y modelos.
- Implementar consulta de canchas y disponibilidad.
- Implementar creación transaccional y prevención de solapamientos.
- Rotar roles: Carlos como Product / Spec Lead y Gabriel como Architecture / Development Lead.

## Ciclo 3 - Operación y calidad

- Incorporar cancelaciones, bloqueos y auditoría.
- Completar interfaz y datos de demostración.
- Ampliar pruebas y automatización.
- Preparar la incorporación de David al rol QA / DevOps.

## Punto de cambio de especificación

Después de completar la reserva mínima se solicitó que las cancelaciones de clientes requieran dos horas de anticipación. El ciclo se ejecutará en este orden:

1. Actualizar RF-11, RN-11, HU-06 y CA-11.
2. Añadir una prueba inicialmente fallida para una cancelación tardía.
3. Incorporar la validación en el servicio transaccional.
4. Reflejar la elegibilidad en la vista de reservas.
5. Ejecutar la suite completa y conservar el resultado en el historial.

## Condición de cierre

- Requisitos críticos trazados a criterios y pruebas.
- Suite completa aprobada.
- Issues y Pull Requests cerrados con evidencia.
- README reproducible.
- Registro de IA y decisiones actualizado.
- Demostración preparada para cualquier integrante.

