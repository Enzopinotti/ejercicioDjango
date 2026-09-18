# B1 — Reproducible runtime and repository hygiene

## Decision

B1 selects:

- Python `3.12.14`;
- Django `5.2.17`;
- asgiref `3.12.1`;
- sqlparse `0.6.0`.

Django 5.2 is the LTS maintenance line chosen for this small academic project. It preserves the historically evidenced Python 3.12 runtime while moving away from unsupported Django 5.0.

## Candidate evidence

Probe SHA:

`83c76b1b4dbb0fe39536144595e1ff5c615660e4`

Workflow run:

`35363207682`

Artifact:

- id: `10555357331`;
- digest: `sha256:81f89153a16a745f0b0c20b9dbf15255ee2084d6ebc7731d28cee6ca251cc09b`.

The candidate proved:

- exact Python `3.12.14`;
- Django `5.2.17`;
- fresh SQLite creation from migrations;
- 13 expected tables after migration;
- 19 migration records;
- empty fresh polls/auth state before smoke seeding;
- `manage.py check` success;
- no model/migration drift;
- existing test command succeeds (still 0 tests; B2 owns tests);
- polls index, static CSS, admin redirect, detail and results smoke succeed;
- dependency audit reports **0 vulnerability findings**;
- historical source remains untouched by the probe.

## Dependency authority

`requirements.txt` pins the complete verified runtime graph rather than leaving Django implicit:

```text
asgiref==3.12.1
Django==5.2.17
sqlparse==0.6.0
```

`.python-version` pins `3.12.14`.

## Repository hygiene

B0 proved that the repository tracked 12 `.pyc` files and a stateful SQLite database.

B1 removes from maintained Git authority:

- every tracked `__pycache__/*.pyc`;
- `trabajocero/db.sqlite3`.

The database contained 3 questions, 5 choices, 1 auth user and 2 sessions at B0. Those row values are not exported or preserved in docs.

Schema truth remains in Django migrations. A clean checkout can reconstruct the database using:

```bash
cd trabajocero
python manage.py migrate
```

`.gitignore` now excludes Python caches, virtual environments, local SQLite state, local environment files and coverage/test artifacts.

## Permanent B1 quality contract

`.github/workflows/quality.yml` verifies:

1. exact Python version;
2. exact requirements installation;
3. no tracked Python cache/bytecode/SQLite state;
4. Django system check;
5. migration drift check;
6. clean-database migration reconstruction;
7. existing Django test command;
8. dependency security audit;
9. clean tracked Git diff after checks.

Actions used in the permanent workflow are SHA-pinned.

## Configuration boundary

B1 does not convert the exercise into a deployment configuration.

The generated development `SECRET_KEY`, `DEBUG=True` and empty `ALLOWED_HOSTS` are already characterized by B0's `check --deploy` warnings. They remain part of the local tutorial configuration for now.

B3 owns framework/config maintenance if tests justify further change.

## Non-adoptions

B1 does not:

- change models;
- change routes or views;
- add application behavior;
- move away from SQLite;
- add Docker;
- introduce a frontend framework;
- invent production deployment.

## Exit

B1 is complete when the materialized exact head passes permanent Quality from a clean checkout.

B2 then owns deterministic polls behavior tests.
