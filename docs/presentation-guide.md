# Guía breve de presentación

## 1. Problema y outcome

- Las reservas coordinadas por mensajes causan demoras y cruces de horario.
- El outcome es permitir que el cliente encuentre y confirme disponibilidad sin intervención manual.

## 2. Recorrido ODD a SDD

1. Mostrar `specs/outcomes.md`.
2. Explicar requisitos y reglas críticas.
3. Mostrar HU-01 a HU-12 y la matriz de trazabilidad.
4. Señalar Issues, ramas, PR y GitHub Actions.

## 3. Demostración funcional

1. Abrir la portada y señalar el próximo horario libre real.
2. Elegir una cancha y una fecha en el calendario.
3. Comparar horarios disponibles y ocupados.
4. Iniciar sesión con `demo_user / demo1234`.
5. Confirmar una reserva y abrir "Mis reservas".
6. Mostrar próxima reserva, historial y política de cancelación.
7. Abrir `/admin/` con `admin_user / admin1234` para enseñar canchas, bloqueos y auditoría.

## 4. Cambio inesperado

- Solicitud: impedir cancelaciones de clientes en las dos horas previas.
- Evidencia: RF-11, RN-11, CA-11, Issue #9 y PR #24.
- Resultado: rechazo sin mutación, explicación al cliente y excepción administrativa.

## 5. Calidad y cierre

- Ejecutar o mostrar GitHub Actions.
- Indicar 58 pruebas aprobadas.
- Resaltar la prueba obligatoria de doble reserva.
- Mencionar la revisión móvil, accesibilidad por teclado y participación de los tres integrantes.

## Respuestas rápidas ante una petición de cambio

- Actualizar primero el requisito y criterio de aceptación.
- Crear o actualizar el Issue.
- Añadir una prueba que reproduzca el nuevo comportamiento.
- Implementar en una rama independiente.
- Abrir un PR y no integrar hasta que GitHub Actions apruebe.
