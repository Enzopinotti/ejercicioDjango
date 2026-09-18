# B5 — Permanent CI, docs and delivery contract

## Goal

Close the modernization lane with one reproducible, reviewable contract from clean checkout through a real HTTP smoke.

## Permanent Quality gate

The final workflow runs on:

- pull requests to `main`;
- pushes to `main`;
- pushes to `modernize/2026-django-quality`;
- manual dispatch.

It verifies:

1. exact Python `3.12.14`;
2. exact requirements installation + `pip check`;
3. repository hygiene;
4. environment-backed settings contract;
5. Django system check;
6. no model/migration drift;
7. clean SQLite reconstruction from migrations;
8. the 25-test behavior/accessibility/admin suite;
9. real `runserver` HTTP smoke;
10. dependency audit;
11. tracked Git tree remains unchanged.

The workflow emits a SHA-specific evidence artifact on every run.

## HTTP delivery smoke

The gate creates only ephemeral local data and starts the real Django development server.

It asserts:

- `/polls/` → 200;
- static polls CSS → 200;
- anonymous `/admin/` → 302;
- published question detail → 200;
- published question results → 200;
- published question appears in the index;
- future question does not appear in the index.

The local SQLite file is ignored and is never committed back to the repository.

## Dependency maintenance

Dependabot is configured monthly for:

- pip;
- GitHub Actions.

Minor/patch updates are grouped to keep noise low.

## Review/merge gate

The lane may merge only after:

- exact branch head Quality is green;
- full diff review against `b2fc80368aa0749ca005d4efc508f6ba638083b4`;
- no generated/cache/local-database state is present;
- PR Quality is green on the reviewed head;
- zero unresolved review threads;
- squash merge uses `expected_head_sha`;
- post-merge `main` Quality is green;
- central portfolio roadmap is synchronized.

## Maintained product truth

This remains:

- an academic Django polls exercise;
- SQLite-based;
- server-rendered;
- locally runnable;
- intentionally small.

There is no production deployment authority in this repository.

## Explicit non-adoptions

The completed lane does not add:

- REST/GraphQL API;
- React/Vue;
- PostgreSQL;
- Docker/Kubernetes;
- custom authentication;
- cloud deployment architecture;
- speculative product features.
