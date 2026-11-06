# Modelo de datos

## Entidades iniciales

### User

Se utilizará el modelo de usuario de Django. Los datos adicionales deben mantenerse al mínimo.

### Court

- `id`
- `name`
- `description`
- `is_active`
- `opening_time`
- `closing_time`

### Booking

- `id`
- `user_id`
- `court_id`
- `starts_at`
- `ends_at`
- `status`: `confirmed` o `cancelled`
- `created_at`
- `cancelled_at`

### CourtBlock

- `id`
- `court_id`
- `starts_at`
- `ends_at`
- `reason`
- `created_by_id`

### AuditEvent

- `id`
- `actor_id`
- `event_type`
- `entity_type`
- `entity_id`
- `details`
- `created_at`

## Restricciones

- `starts_at < ends_at`.
- Las reservas canceladas no bloquean disponibilidad.
- Las comprobaciones de conflicto se realizan dentro de una transacción.
- Los registros de auditoría no deben guardar contraseñas ni datos sensibles innecesarios.

