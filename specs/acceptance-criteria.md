# Criterios de aceptación

- **CA-01:** Dada una cancha activa, cuando el visitante consulta una fecha válida, entonces recibe sus horarios disponibles y ocupados.
- **CA-02:** Dado un usuario autenticado y un horario libre, cuando solicita una reserva válida, entonces se crea una única reserva confirmada.
- **CA-03:** Dada una reserva activa, cuando otro usuario solicita un intervalo que se superpone, entonces la solicitud es rechazada y no se modifica la disponibilidad.
- **CA-04:** Dadas dos reservas consecutivas sin superposición, cuando se registra la segunda, entonces ambas permanecen válidas.
- **CA-05:** Dado un bloqueo administrativo, cuando se solicita una reserva que lo intersecta, entonces la solicitud es rechazada.
- **CA-06:** Dada una fecha pasada o un intervalo inválido, cuando se intenta reservar, entonces se devuelve un error de validación sin crear una reserva.
- **CA-07:** Dada una reserva propia y cancelable, cuando el usuario la cancela, entonces cambia a cancelada y libera el horario.
- **CA-08:** Dada una reserva ajena, cuando un usuario intenta cancelarla, entonces recibe una respuesta de acceso denegado y el estado no cambia.
- **CA-09:** Dado un conflicto, cuando se rechaza la solicitud, entonces el usuario recibe la causa y al menos una alternativa cuando existan horarios cercanos.
- **CA-10:** Dada una acción de creación, cancelación o bloqueo, cuando concluye, entonces queda registrada para auditoría.

## Criterio obligatorio de doble reserva

CA-03 debe contar con una prueba automatizada independiente y ejecutarse en integración continua.

