import os

import django

SECRET_KEY = "jsonstore-test-key-not-a-secret"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "tests.apps.TestsConfig",
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

# Point DATABASE_URL at postgres/mysql/oracle to exercise the queries that need
# first-class JSONField support; sqlite covers the model and form API.
# `docker compose up -d` starts all of them -- see docker-compose.yml.
if os.environ.get("DATABASE_URL"):
    import dj_database_url

    DATABASES = {"default": dj_database_url.config()}

    if "oracle" in DATABASES["default"]["ENGINE"]:
        oracle = DATABASES["default"]
        # With PORT set, Django builds the DSN as makedsn(host, port, sid) --
        # and the container publishes a *service* name, not a SID. Pass the
        # whole "host:port/service" string as NAME instead, which Django uses
        # verbatim when PORT is empty.
        if oracle["PORT"]:
            oracle["NAME"] = "%s:%s/%s" % (
                oracle["HOST"] or "localhost",
                oracle["PORT"],
                oracle["NAME"],
            )
            oracle["HOST"] = ""
            oracle["PORT"] = ""
        # Oracle's test runner creates a dedicated user and tablespace rather
        # than a database, and needs to be told which ones to use.
        oracle["TEST"] = {
            "USER": "test_jsonstore",
            "PASSWORD": "jsonstore",
            "TBLSPACE": "test_jsonstore",
            "TBLSPACE_TMP": "test_jsonstore_temp",
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(
                BASE_DIR, "..", "dj{}{}.sqlite3".format(*django.VERSION[:2])
            ),
        }
    }

# The test models are declared inside the test modules and have no migrations.
MIGRATION_MODULES = {"tests": None}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

USE_TZ = True

TIME_ZONE = "UTC"

LANGUAGE_CODE = "en-us"

USE_I18N = True
