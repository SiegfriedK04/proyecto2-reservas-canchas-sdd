# Lista de cumplimiento del Proyecto 2

Esta lista relaciona las restricciones de la asignación con evidencia verificable del repositorio.

| Requisito | Estado | Evidencia |
|---|---|---|
| Repositorio Git | Cumplido | Repositorio `proyecto2-reservas-canchas-sdd` bajo la propiedad de Gabriel Rodríguez. |
| Estructura de referencia | Cumplido | `README.md`, `specs/`, `docs/`, aplicación `reservations/` y sus pruebas. |
| Issues | Cumplido | Issues #1 a #30; backlog funcional HU-01 a HU-12. |
| Commits identificables | Cumplido | Commits convencionales `docs`, `feat`, `fix` y `test`. |
| Ramas | Cumplido | Ramas de documentación, funcionalidad, corrección, pruebas y mantenimiento. |
| Pull Requests y revisión | Cumplido | PR #10, #11, #21 a #24 y #31 a #35, con revisión cruzada. |
| Pruebas automatizadas | Cumplido | 58 pruebas de modelos, servicios, vistas, API y criterios de aceptación. |
| Historial de cambios | Cumplido | `docs/change-history.md`. |
| README | Cumplido | Instalación, uso, arquitectura, pruebas, seguridad y evidencias. |
| Libertad tecnológica documentada | Cumplido | `specs/architecture.md` describe Python, Django, SQLite y límites. |
| AI Development Log | Cumplido | `docs/ai-log.md` registra actividad, IA, solicitud, resultado y decisión. |
| Testing obligatorio | Cumplido | Doble reserva, conflictos, validaciones de usuario y criterios cuentan con pruebas. |
| Cambio inesperado | Cumplido | Ventana de cancelación: especificación, criterio, plan, prueba fallida, código y resultado. |
| Rotación de roles | Cumplido | `docs/roles.md` muestra los ciclos de Gabriel, Carlos y David. |
| Material de presentación | Cumplido | `docs/presentation-guide.md` y la aplicación funcional. |

## Estructura recomendada

La asignación presenta `src/` y `tests/` como referencia, no como nombres obligatorios. En la convención de Django utilizada, el código reside en `reservations/` y las pruebas en `reservations/tests/`. Los documentos solicitados conservan sus nombres dentro de `specs/` y `docs/`.

## Verificación final

```text
python manage.py check                              -> sin observaciones
python manage.py makemigrations --check --dry-run   -> sin cambios pendientes
python manage.py test                               -> 58 pruebas aprobadas
```
