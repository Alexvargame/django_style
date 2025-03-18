import environ, os
from django.core.exceptions import ImproperlyConfigured
from pathlib import Path

env = environ.Env()
#
# BASE_DIR = environ.Path(__file__) - 2
# APPS_DIR = BASE_DIR.path("education_apps")

BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = os.path.join(BASE_DIR, "education_apps")

def env_to_enum(enum_cls, value):
    for x in enum_cls:
        if x.value == value:
            return x

    raise ImproperlyConfigured(f"Env value {repr(value)} could not be found in {repr(enum_cls)}")