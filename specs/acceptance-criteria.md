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
- **CA-11:** Dada una reserva que inicia en menos de dos horas, cuando el cliente intenta cancelarla, entonces el sistema conserva la reserva y explica el límite; un administrador sí puede cancelarla por operación.
- **CA-12:** Dado un usuario en una pantalla de 390 px o que navega con teclado, cuando recorre la interfaz, entonces encuentra los enlaces de su cuenta, ve el foco y el menú indica la página actual con `aria-current="page"`.
- **CA-13:** Dado un cliente con reservas próximas, finalizadas y canceladas, cuando abre su agenda, entonces ve la próxima destacada, las próximas en orden ascendente y las demás en el historial, sin avisos de cancelación en reservas finalizadas.
- **CA-14:** Dado un horario reservado o bloqueado, cuando se consulta la disponibilidad, entonces aparece como ocupado, no puede seleccionarse y no revela el usuario ni el motivo.
- **CA-15:** Dadas canchas activas con horarios libres, cuando un visitante abre la portada, entonces ve el primer horario libre real y su enlace abre el calendario en esa fecha.

## Criterio obligatorio de doble reserva

CA-03 debe contar con una prueba automatizada independiente y ejecutarse en integración continua.

