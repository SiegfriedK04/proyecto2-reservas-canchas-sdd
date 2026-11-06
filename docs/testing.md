# Estrategia de pruebas

## Niveles

- Pruebas unitarias para validadores y cálculo de solapamientos.
- Pruebas de modelo para restricciones y cambios de estado.
- Pruebas de servicio para creación transaccional.
- Pruebas de vistas y API para autenticación, permisos y mensajes.
- Pruebas de criterios de aceptación para recorridos completos.

## Casos críticos iniciales

1. Crear una reserva válida.
2. Rechazar una doble reserva exacta.
3. Rechazar solapamiento parcial por el inicio.
4. Rechazar solapamiento parcial por el final.
5. Rechazar una reserva que contiene completamente a otra.
6. Permitir intervalos consecutivos.
7. Rechazar un bloqueo administrativo.
8. Rechazar fecha pasada e intervalo invertido.
9. Cancelar una reserva propia.
10. Impedir cancelar una reserva ajena.
11. Confirmar que un rechazo no altera el estado.
12. Verificar la alternativa propuesta ante un conflicto.

## Integración continua

GitHub Actions ejecutará comprobaciones y pruebas en cada Pull Request y actualización de `main`. Ningún cambio funcional se integrará con pruebas fallidas.

## Evidencia

Cada Pull Request debe incluir los comandos ejecutados y relacionar las pruebas con los criterios de aceptación afectados.

## Resultado del ciclo de interfaz y reservas

- `python manage.py check`: sin observaciones.
- `python manage.py test`: 30 pruebas aprobadas.
- Revisión visual: inicio, calendario, inicio de sesión y registro verificados en escritorio.
- Calendario: 42 celdas mensuales, navegación entre meses y horarios obtenidos desde la API.
- Datos demo: ejecución repetible y permisos del administrador verificados.
- Administración: canchas, reservas, bloqueos y auditoría registrados en el panel.
- Integración continua: configuración preparada para ejecutar comprobaciones y pruebas en cada Pull Request.
- Cambio de especificación: cancelación tardía rechazada sin mutación y excepción administrativa verificadas.

