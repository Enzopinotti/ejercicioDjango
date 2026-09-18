# B3 — Configuration and maintained runtime boundary

## Scope

B3 does not add production infrastructure. It makes the existing local-learning configuration explicit and removes the repository-specific generated secret from source control.

B1 already selected the maintained framework runtime:

- Python `3.12.14`;
- Django `5.2.17` LTS;
- dependency audit: 0 findings.

B3 therefore does **not** perform another framework upgrade.

## Starting problem

The historical `settings.py` committed:

- one concrete `django-insecure-...` generated secret;
- `DEBUG=True`;
- `ALLOWED_HOSTS=[]`.

B0 correctly reported Django deploy-check warnings. Those warnings demonstrated that this was local tutorial configuration, but the specific generated key did not need to remain the maintained source authority.

## Maintained configuration

The settings now support:

- `DJANGO_SECRET_KEY`;
- `DJANGO_DEBUG`;
- `DJANGO_ALLOWED_HOSTS`.

Defaults remain deliberately local:

- secret: explicit local-only non-production fallback;
- debug: enabled;
- allowed hosts: `127.0.0.1,localhost`.

This preserves a zero-configuration learning experience:

```bash
cd trabajocero
python manage.py migrate
python manage.py runserver
```

while allowing callers to override the three settings without editing tracked Python source.

## Why deploy warnings are not blindly silenced

This repository has no production deployment requirement.

B3 does not enable HSTS, force HTTPS, or mark cookies secure merely to make `check --deploy` visually green. Those settings require a real HTTPS deployment boundary and would be misleading in a local tutorial.

The local-only fallback secret intentionally remains visibly non-production.

## Deterministic contract

`scripts/config_contract.py` starts fresh Python/Django processes and verifies:

1. local defaults;
2. secret override;
3. debug disable override;
4. comma-separated allowed-host override;
5. accepted truthy debug form.

The contract never prints the secret value.

Permanent Quality runs this contract before Django system checks.

## Security/truth boundary

B3 removes the repository-specific 2025 generated secret from maintained source.

It does not claim historical Git data can be erased by a new commit. The previous value remains part of repository history, but it belonged to a public local-learning settings file and is not treated as a production credential.

## Non-adoptions

B3 does not:

- add `python-dotenv`;
- require a `.env` file;
- add a deployment provider;
- force HTTPS;
- configure HSTS;
- move away from SQLite;
- add authentication features.

## Exit

B3 is complete when exact-head Quality passes:

- runtime identity;
- dependency install;
- repository hygiene;
- configuration contract;
- Django check;
- migration reconstruction/drift check;
- 17 behavior tests;
- dependency audit;
- clean tracked tree.
