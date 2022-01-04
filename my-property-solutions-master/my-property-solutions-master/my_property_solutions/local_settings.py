# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#g(5zv-!kie@0l%&*8ubyv0h(%#l2vie*4=804x0kdi3$4!u)m'
# To generate a secret key try:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

ALLOWED_HOSTS = ['3.25.115.118','*']  # List of strings of allowed hosts

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "my_property_solutions",
        "HOST": "localhost",
        "USER" : "postgres",
        "PORT": 5432,
        "PASSWORD": "12345"
    }
}

from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="",
    integrations=[DjangoIntegration()],
    environment="dev",
)


# if DEBUG:
#
#     INSTALLED_APPS += ["debug_toolbar"]
#
#     MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
#
#     DEBUG_TOOLBAR_PANELS = [
#         "debug_toolbar.panels.versions.VersionsPanel",
#         "debug_toolbar.panels.timer.TimerPanel",
#         "debug_toolbar.panels.settings.SettingsPanel",
#         "debug_toolbar.panels.headers.HeadersPanel",
#         "debug_toolbar.panels.request.RequestPanel",
#         "debug_toolbar.panels.sql.SQLPanel",
#         "debug_toolbar.panels.staticfiles.StaticFilesPanel",
#         "debug_toolbar.panels.templates.TemplatesPanel",
#         "debug_toolbar.panels.cache.CachePanel",
#         "debug_toolbar.panels.signals.SignalsPanel",
#         "debug_toolbar.panels.logging.LoggingPanel",
#         "debug_toolbar.panels.redirects.RedirectsPanel",
#     ]
#
#     INTERNAL_IPS = ["127.0.0.1"]
