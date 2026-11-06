# Historias de usuario

Las historias se numeran para mantener trazabilidad entre backlog, requisitos, criterios, ramas y Pull Requests.

## HU-01 - Explorar canchas

**Como** visitante, **quiero** consultar las canchas activas y sus características, **para** escoger la opción adecuada antes de reservar.

### Criterios

- Se muestran nombre, descripción, ubicación y horario operativo.
- Una cancha inactiva no aparece en el catálogo público.
- Se puede abrir directamente la vista de disponibilidad.

**Trazabilidad:** RF-01, CA-01.

## HU-02 - Crear una cuenta

**Como** cliente nuevo, **quiero** registrarme e iniciar sesión, **para** gestionar reservas asociadas con mi identidad.

### Criterios

- El correo se normaliza y no se permite duplicarlo.
- La contraseña se gestiona mediante los mecanismos de Django.
- Después del registro el usuario queda autenticado.

**Trazabilidad:** RF-02, RNF-03.

## HU-03 - Consultar disponibilidad en un calendario

**Como** cliente, **quiero** seleccionar un día desde un calendario mensual y ver horarios disponibles, **para** encontrar una opción sin intercambiar mensajes con el administrador.

### Criterios

- La navegación mensual funciona sin recargar toda la página.
- El día seleccionado se distingue visualmente.
- Los horarios disponibles se presentan en una cuadrícula.
- El resumen muestra cancha, fecha, hora y duración antes de continuar.

**Trazabilidad:** RF-03, CA-01.

## HU-04 - Confirmar una reserva

**Como** usuario autenticado, **quiero** reservar una cancha en un horario disponible, **para** asegurar mi espacio.

### Criterios

- La selección requiere fecha y horario válidos.
- La creación se realiza de forma atómica.
- El usuario recibe confirmación y puede consultar la reserva.

**Trazabilidad:** RF-04, CA-02.

## HU-05 - Evitar conflictos de horario

**Como** administrador, **quiero** que el sistema rechace reservas superpuestas, **para** evitar prometer la misma cancha a dos clientes.

### Criterios

- Se rechazan coincidencias exactas y solapamientos parciales o totales.
- Se permiten intervalos consecutivos según la especificación inicial.
- Un rechazo no modifica la base de datos.
- La regla cuenta con una prueba automatizada independiente.

**Trazabilidad:** RF-05, RN-01, CA-03, CA-04.

## HU-06 - Gestionar mis reservas

**Como** cliente, **quiero** consultar y cancelar mis reservas elegibles, **para** mantener mis compromisos actualizados.

### Criterios

- Solo se muestran datos privados del usuario autenticado.
- El cliente no puede cancelar una reserva ajena.
- Una cancelación libera disponibilidad y conserva historial.

**Trazabilidad:** RF-06, CA-07, CA-08.

## HU-07 - Administrar canchas y bloqueos

**Como** administrador, **quiero** gestionar canchas y bloquear períodos, **para** reflejar mantenimiento o indisponibilidad operativa.

### Criterios

- El administrador puede crear, editar y desactivar canchas.
- Un bloqueo impide confirmar reservas que lo intersecten.
- La razón del bloqueo se conserva para auditoría.

**Trazabilidad:** RF-07, CA-05.

## HU-08 - Comprender un rechazo

**Como** cliente, **quiero** conocer por qué una solicitud fue rechazada y ver alternativas, **para** completar la reserva sin comenzar de nuevo.

### Criterios

- El mensaje utiliza lenguaje claro y un código estable.
- Los datos válidos permanecen seleccionados.
- Se muestran horarios alternativos cuando existen.
- No se revela la identidad de otros clientes.

**Trazabilidad:** RF-08, RF-09, CA-09.

## HU-09 - Auditar la operación

**Como** administrador, **quiero** consultar eventos de creación, cancelación y bloqueo, **para** investigar cambios y resolver incidentes.

### Criterios

- Cada evento conserva actor, tipo, entidad y fecha.
- La auditoría no almacena contraseñas ni datos innecesarios.
- Los registros no se eliminan al cancelar una reserva.

**Trazabilidad:** RF-10, CA-10.

