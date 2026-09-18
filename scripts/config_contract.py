from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "trabajocero"

PROBE = """
from django.conf import settings
print(f"debug={int(settings.DEBUG)}")
print("hosts=" + ",".join(settings.ALLOWED_HOSTS))
print(f"secret_is_expected={int(settings.SECRET_KEY == EXPECTED_SECRET)}")
"""

def probe(env_updates, expected_secret):
    env = os.environ.copy()
    for key in ("DJANGO_SECRET_KEY", "DJANGO_DEBUG", "DJANGO_ALLOWED_HOSTS"):
        env.pop(key, None)
    env.update(env_updates)
    env["DJANGO_SETTINGS_MODULE"] = "trabajocero.settings"

    script = f"EXPECTED_SECRET={expected_secret!r}\n" + PROBE
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=PROJECT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return dict(
        line.split("=", 1)
        for line in result.stdout.strip().splitlines()
    )

default_secret = "django-insecure-local-development-only-not-for-production"
default = probe({}, default_secret)
assert default == {
    "debug": "1",
    "hosts": "127.0.0.1,localhost",
    "secret_is_expected": "1",
}, default

override_secret = "b3-test-only-secret-not-a-real-credential"
overridden = probe(
    {
        "DJANGO_SECRET_KEY": override_secret,
        "DJANGO_DEBUG": "0",
        "DJANGO_ALLOWED_HOSTS": "example.test, api.example.test",
    },
    override_secret,
)
assert overridden == {
    "debug": "0",
    "hosts": "example.test,api.example.test",
    "secret_is_expected": "1",
}, overridden

truthy = probe(
    {
        "DJANGO_SECRET_KEY": override_secret,
        "DJANGO_DEBUG": "yes",
        "DJANGO_ALLOWED_HOSTS": "localhost",
    },
    override_secret,
)
assert truthy["debug"] == "1", truthy

print("B3 configuration contract passed.")
print("default-debug=1")
print("default-hosts=127.0.0.1,localhost")
print("secret-override=supported")
print("debug-override=supported")
print("hosts-override=supported")
