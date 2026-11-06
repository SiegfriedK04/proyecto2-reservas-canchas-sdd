# Resultados ODD

## Contexto de descubrimiento

El escenario inicial representa una operación pequeña o mediana de canchas deportivas que todavía coordina parte de sus reservas mediante mensajes y revisión manual del calendario. Las respuestas siguientes son hipótesis de trabajo basadas en los problemas observados durante el Proyecto 1. Deben validarse durante el desarrollo y ajustarse si aparecen nuevas evidencias.

## Preguntas y respuestas iniciales

### 1. ¿Cómo se reservan actualmente las canchas?

El cliente escribe por WhatsApp, llama o consulta directamente al encargado. El administrador revisa un calendario, una agenda o una lista interna, propone horarios y registra la reserva manualmente. La confirmación depende de que el encargado responda y actualice la información.

### 2. ¿Qué causa los conflictos de horario?

Los conflictos aparecen cuando existen varios canales de atención, el calendario no se actualiza inmediatamente, dos personas consultan el mismo espacio al mismo tiempo o una reserva recurrente se registra sin comprobar todas sus fechas. También influyen los cambios comunicados de manera informal y la falta de una validación central antes de confirmar.

### 3. ¿Quién confirma o cancela una reserva?

Actualmente el administrador confirma la reserva después de revisar la disponibilidad. Para cancelar, el cliente envía una solicitud y el administrador modifica la agenda. En el sistema propuesto, el cliente podrá cancelar sus propias reservas dentro de la política aprobada y el administrador conservará facultades para bloquear horarios, confirmar excepciones y consultar la auditoría.

### 4. ¿Cuánto tarda el usuario en encontrar disponibilidad?

La hipótesis inicial es de 5 a 15 minutos cuando el encargado está disponible, con demoras mayores fuera del horario de atención o cuando deben intercambiarse varios mensajes. El resultado esperado es que el usuario encuentre alternativas válidas en menos de dos minutos sin intervención del personal.

### 5. ¿Qué información necesita el administrador?

Necesita conocer canchas, horarios de operación, bloqueos, reservas activas, datos mínimos del cliente, estado de cada reserva, cancelaciones, conflictos rechazados, demanda por franja horaria y un historial que permita saber quién realizó cada cambio.

### 6. ¿Qué debe ocurrir cuando una reserva es rechazada?

El sistema no debe crear registros parciales ni ocupar el horario. Debe explicar la causa con lenguaje claro, conservar los datos válidos ingresados, mostrar horarios alternativos y permitir que el usuario vuelva a intentarlo. El rechazo debe quedar disponible para diagnóstico sin exponer datos de otros clientes.

## Problema

Los clientes dependen de la disponibilidad del administrador para conocer horarios y pueden producirse cruces porque la información se distribuye entre mensajes, llamadas y registros manuales.

## Resultado principal

Reducir los conflictos de horario y permitir que el cliente encuentre y reserve una cancha disponible sin intervención manual, manteniendo control operativo y trazabilidad para el administrador.

## Resultados medibles iniciales

- El usuario encuentra un horario disponible en menos de dos minutos durante una prueba guiada.
- Ninguna solicitud aceptada genera una doble reserva para la misma cancha y franja horaria.
- Todo rechazo informa una causa y no modifica la disponibilidad.
- El administrador puede identificar reservas, cancelaciones y bloqueos desde una única fuente.
- Las reglas críticas cuentan con criterios de aceptación y pruebas automatizadas.

## Fuera del alcance inicial

- Pagos en línea.
- Integraciones con cerraduras o iluminación física.
- Aplicación móvil nativa.
- Facturación fiscal.
- Reservas para organizaciones con múltiples sucursales.

