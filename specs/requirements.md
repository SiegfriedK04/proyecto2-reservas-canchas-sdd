# Requisitos

## Requisitos funcionales

- **RF-01:** El sistema debe mostrar las canchas disponibles y su información básica.
- **RF-02:** El usuario debe poder crear una cuenta e iniciar sesión.
- **RF-03:** El usuario debe poder consultar disponibilidad por cancha y fecha.
- **RF-04:** El usuario autenticado debe poder crear una reserva indicando cancha, fecha, hora inicial y hora final.
- **RF-05:** El sistema debe rechazar cualquier reserva que se superponga con una reserva o bloqueo activo de la misma cancha.
- **RF-06:** El usuario debe poder consultar sus reservas y cancelar las elegibles.
- **RF-07:** El administrador debe poder crear bloqueos operativos y consultar todas las reservas.
- **RF-08:** Ante un rechazo, el sistema debe informar la causa y conservar el estado previo.
- **RF-09:** El sistema debe mostrar alternativas próximas cuando el horario solicitado no esté disponible.
- **RF-10:** Las cancelaciones y cambios administrativos deben quedar registrados.

## Requisitos no funcionales

- **RNF-01:** Las reglas de integridad deben validarse en el servidor.
- **RNF-02:** Las operaciones de creación de reservas deben ser atómicas.
- **RNF-03:** Un usuario no debe acceder a datos privados de reservas ajenas.
- **RNF-04:** Las reglas críticas deben contar con pruebas automatizadas.
- **RNF-05:** La interfaz debe poder utilizarse en computadora y dispositivo móvil.
- **RNF-06:** La ejecución local debe poder iniciarse con instrucciones reproducibles.
- **RNF-07:** Cada cambio funcional debe relacionarse con un Issue, una rama y una revisión.

## Dependencias de aprobación

La implementación de RF-04 y RF-05 no debe comenzar hasta aprobar las reglas de solapamiento, duración y horario operativo en `business-rules.md`.

