import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Read .env values (root folder) so aHost/prod configs are picked up automatically
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

_default_hosts = ["bilimstore.uz", "www.bilimstore.uz", "127.0.0.1", "localhost"]
_allowed_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", ",".join(_default_hosts))
ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts.split(",") if h.strip()] or _default_hosts

_default_csrf = "https://bilimstore.uz,https://www.bilimstore.uz"
_csrf_origins = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", _default_csrf)
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in _csrf_origins.split(",") if origin.strip()]

SECURE_SSL_REDIRECT = os.environ.get(
    "DJANGO_SECURE_SSL_REDIRECT",
    "True" if not DEBUG else "False",
).lower() == "true"
SESSION_COOKIE_SECURE = os.environ.get("DJANGO_SESSION_COOKIE_SECURE", str(not DEBUG)).lower() == "true"
CSRF_COOKIE_SECURE = os.environ.get("DJANGO_CSRF_COOKIE_SECURE", str(not DEBUG)).lower() == "true"
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_SECURE_HSTS_SECONDS", "31536000" if SECURE_SSL_REDIRECT else "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    str(SECURE_SSL_REDIRECT),
).lower() == "true"
SECURE_HSTS_PRELOAD = os.environ.get("DJANGO_SECURE_HSTS_PRELOAD", str(SECURE_SSL_REDIRECT)).lower() == "true"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "apps.catalog",
    "apps.orders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'backend.backend.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.orders.context_processors.cart",
                "apps.catalog.context_processors.categories",
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.backend.wsgi.application'

# DB: default to SQLite for easy deploys (aHost friendly).
# Switch to Postgres by setting DJANGO_DB_ENGINE=postgres in the environment.
_db_engine = os.environ.get("DJANGO_DB_ENGINE", "sqlite").lower()
if _db_engine in {"postgres", "postgresql"}:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "bookstore_db"),
            "USER": os.environ.get("POSTGRES_USER", "bookuser"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "StrongPassword123"),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
            "OPTIONS": {
                "options": "-c client_encoding=UTF8",
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "uz"
LANGUAGES = [
    ("uz", "O‘zbekcha"),
]
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Cache: default to local memory (can be swapped to Redis/Memcached via env)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "bilim-cache",
    }
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CART_SESSION_ID = "cart"

# Delivery configuration (coordinates: decimal degrees)
SHOP_LAT = float(os.environ.get("SHOP_LAT", "41.2995"))
SHOP_LNG = float(os.environ.get("SHOP_LNG", "69.2401"))
DELIVERY_BASE_FEE_UZS = int(os.environ.get("DELIVERY_BASE_FEE_UZS", "10000"))
DELIVERY_PER_KM_FEE_UZS = int(os.environ.get("DELIVERY_PER_KM_FEE_UZS", "2000"))
DELIVERY_MIN_FEE_UZS = int(os.environ.get("DELIVERY_MIN_FEE_UZS", "10000"))
DELIVERY_MAX_FEE_UZS = int(os.environ.get("DELIVERY_MAX_FEE_UZS", "60000"))
DELIVERY_FREE_OVER_UZS = os.environ.get("DELIVERY_FREE_OVER_UZS")
if DELIVERY_FREE_OVER_UZS is not None and DELIVERY_FREE_OVER_UZS != "":
    DELIVERY_FREE_OVER_UZS = int(DELIVERY_FREE_OVER_UZS)
else:
    DELIVERY_FREE_OVER_UZS = None

# Upload memory usage: force temp files instead of RAM to save memory footprint.
FILE_UPLOAD_HANDLERS = ["django.core.files.uploadhandler.TemporaryFileUploadHandler"]
FILE_UPLOAD_MAX_MEMORY_SIZE = 0  # always stream to disk
