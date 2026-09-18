# Actividad 0 — Introducción a Git y Django

Ejercicio académico realizado por **Enzo Pinotti** para la materia **Ingeniería de Software — UTN FRLP**.

El repositorio conserva la progresión original de abril de 2025 y mantiene el ejemplo clásico de encuestas de Django sin convertirlo en un producto distinto.

## Stack mantenido

- Python `3.12.14`;
- Django `5.2.17 LTS`;
- SQLite local reconstruible desde migraciones;
- templates y static files nativos de Django;
- app `polls`;
- GitHub Actions + pip-audit.

La versión histórica se reprodujo como Python 3.12 + Django 5.0 a partir del bytecode y la migración originales. La autoridad 2026 conserva Python 3.12 y usa Django 5.2 LTS.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cd trabajocero
python manage.py migrate
python manage.py runserver
```

Luego:

- encuestas: `http://127.0.0.1:8000/polls/`;
- admin: `http://127.0.0.1:8000/admin/`.

`db.sqlite3` es estado local y no forma parte de la autoridad versionada. Una instalación nueva reconstruye el esquema desde las migraciones.

## Configuración local

La app funciona sin configuración adicional para uso local.

Overrides opcionales:

- `DJANGO_SECRET_KEY`;
- `DJANGO_DEBUG`;
- `DJANGO_ALLOWED_HOSTS` — lista separada por comas.

Los defaults están definidos como **local-learning only**. El repositorio no pretende simular configuración HTTPS/productiva sin una infraestructura real.

## Comportamiento protegido

La suite mantiene **25 tests** sobre:

- recencia de preguntas;
- exclusión de preguntas futuras;
- listado/orden/límite;
- detail/results y 404;
- voto válido, inválido y ausente;
- persistencia del contador;
- semántica de formulario y errores;
- viewport/main landmarks;
- foco visible y reduced motion;
- singular/plural de votos;
- registro y protección del Django admin.

## Quality

Desde la raíz:

```bash
python scripts/quality.py
python scripts/config_contract.py
cd trabajocero
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

El CI permanente además:

- reconstruye una SQLite vacía desde migraciones;
- ejecuta un smoke HTTP contra `runserver`;
- ejecuta `pip-audit`;
- verifica que el árbol trackeado quede limpio;
- publica evidencia específica del SHA.

## Alcance

Este repositorio sigue siendo una actividad de aprendizaje. No se agregan React, API REST, PostgreSQL, Docker, autenticación propia ni infraestructura que el ejercicio no necesita.

## Evidencia de modernización

- [B0 — baseline histórico reproducible](docs/modernization-2026/b0-baseline.md)
- [B1 — runtime reproducible y limpieza de repositorio](docs/modernization-2026/b1-toolchain-hygiene.md)
- [B2 — contratos de comportamiento de polls](docs/modernization-2026/b2-polls-behavior.md)
- [B3 — configuración y runtime mantenido](docs/modernization-2026/b3-configuration-runtime.md)
- [B4 — accesibilidad de templates y admin](docs/modernization-2026/b4-template-accessibility.md)
- [B5 — CI permanente y cierre](docs/modernization-2026/b5-delivery.md)

Programa de portfolio: [Enzopinotti/Enzopinotti#19](https://github.com/Enzopinotti/Enzopinotti/issues/19)
