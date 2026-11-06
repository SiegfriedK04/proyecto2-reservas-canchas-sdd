# Reglas del negocio

- **RN-01:** Una cancha no puede tener dos reservas activas que se superpongan.
- **RN-02:** Un bloqueo administrativo ocupa el horario igual que una reserva activa.
- **RN-03:** La hora final debe ser posterior a la hora inicial.
- **RN-04:** No se aceptan reservas en fechas u horas pasadas.
- **RN-05:** La reserva debe encontrarse dentro del horario de operación de la cancha.
- **RN-06:** Solo usuarios autenticados pueden crear o cancelar reservas.
- **RN-07:** El usuario solo puede cancelar sus propias reservas.
- **RN-08:** Una reserva cancelada deja de bloquear disponibilidad, pero permanece en el historial.
- **RN-09:** Un rechazo no debe crear ni modificar reservas.
- **RN-10:** Los mensajes de disponibilidad no deben revelar la identidad de otros usuarios.

## Regla crítica de solapamiento

Dos intervalos se superponen cuando el inicio de la nueva reserva es anterior al final de una existente y el final de la nueva reserva es posterior al inicio de la existente.

Se permiten reservas consecutivas cuando una comienza exactamente al terminar la anterior, salvo que un cambio posterior de especificación introduzca un tiempo de separación.

