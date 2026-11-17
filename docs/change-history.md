# Historial de cambios

## 2026-11-05 - Fundación

- Se seleccionó el dominio de reservas de canchas.
- Se documentaron las respuestas ODD iniciales.
- Se definieron resultado, métricas, alcance y reglas preliminares.
- Se propuso el stack y la rotación inicial de roles.
- Se preparó el backlog de fundación, especificaciones, arquitectura, implementación y pruebas.
- Se revisó la arquitectura inicial, se documentó el flujo transaccional y se añadió la matriz de trazabilidad.
- Se documentaron nueve historias de usuario numeradas y se enlazaron con requisitos y criterios.
- Se implementaron el dominio de reservas, el catálogo, el registro y la gestión de sesiones.
- Se añadió un calendario mensual interactivo, horarios disponibles, resumen y confirmación.
- Se incorporaron cancelaciones, alternativas ante conflictos, datos demo y 24 pruebas automatizadas.
- Se añadió integración continua y se amplió la suite a 27 pruebas con cobertura del panel administrativo y datos demo.

## Cambio inesperado

### 2026-11-05 - Ventana mínima de cancelación

- **Cambio solicitado:** impedir cancelaciones de clientes durante las dos horas previas a la reserva.
- **Motivo:** dar tiempo al administrador para reasignar el horario y preparar la cancha.
- **Especificación actualizada:** RF-11, RN-11 y HU-06.
- **Criterio actualizado:** CA-11 contempla rechazo sin mutación y excepción administrativa.
- **Plan:** especificación y prueba fallida primero; servicio e interfaz después.
- **Issue:** #9.
- **Código:** el servicio aplica el límite de manera transaccional y conserva una excepción para personal autorizado.
- **Interfaz:** la agenda oculta la acción no elegible y explica que faltan menos de dos horas.
- **Pruebas:** rechazo del cliente, conservación del estado, excepción administrativa y presentación en la agenda.
- **Estado:** implementado y validado.

## Ciclo de mejoras complementarias

### 2026-11-11 - Revisión QA y mejoras de experiencia

- **Origen:** revisión QA de la línea base en escritorio (1366 px) y móvil (390 px), registrada en #25 y #26.
- **Hallazgos:** enlaces de cuenta ocultos en móvil, foco poco visible, horarios ocupados omitidos pese a CA-01, aviso de cancelación en reservas finalizadas, agenda sin orden cronológico y horario fijo en la portada.
- **Especificación agregada:** HU-10, HU-11, HU-12, RF-12, RF-13, RF-14, RNF-08 y CA-12 a CA-15.
- **Plan:** especificación primero; después un Pull Request independiente por Issue (#27, #28, #29 y #30), cada uno con pruebas automatizadas.
- **Compatibilidad:** la API de disponibilidad conserva el campo `slots` y agrega `occupied_slots`.
- **Estado:** especificado; implementación en revisión.

