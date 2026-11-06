# Contrato de API inicial

La interfaz será renderizada principalmente por Django. Los endpoints JSON se limitarán a las operaciones donde mejoren la consulta del calendario.

| Método | Ruta propuesta | Resultado |
|---|---|---|
| `GET` | `/api/courts/` | Lista de canchas activas |
| `GET` | `/api/courts/<id>/availability/?date=AAAA-MM-DD` | Intervalos ocupados y alternativas disponibles |
| `POST` | `/api/bookings/` | Crea una reserva o devuelve un rechazo comprobable |
| `GET` | `/api/bookings/mine/` | Reservas del usuario autenticado |
| `POST` | `/api/bookings/<id>/cancel/` | Cancela una reserva elegible |

## Respuesta de rechazo

```json
{
  "code": "booking_conflict",
  "message": "El horario seleccionado ya no está disponible.",
  "alternatives": []
}
```

Un rechazo debe utilizar un código estable, un mensaje comprensible y no debe crear registros parciales.

