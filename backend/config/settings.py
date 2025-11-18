import os
import environ
from datetime import timedelta
from pathlib import Path

# ==============================
# BASE DIR + ENV LOADING
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ACCESS_TOKEN_LIFETIME_MINUTES=(int, 30),
    REFRESH_TOKEN_DAYS=(int, 7),
)

# Load .env ONLY — never commit .env to Git
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = env.bool("DEBUG", default=True)

if DEBUG:
    # Safe-ish default for local dev only
    SECRET_KEY = env(
        "SECRET_KEY",
        default="dev-secret-key-change-me"
    )
else:
    SECRET_KEY = env("SECRET_KEY")  # must be set in prod

ALLOWED_HOSTS = [
    h.strip() for h in env("ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")
    if h.strip()
]

# ==============================
# APPLICATIONS
# ==============================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "nested_admin",
    "rest_framework",
    "corsheaders",
    "django_filters",
    "api.apps.ApiConfig",
]

# ==============================
# MIDDLEWARE
# ==============================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # Whitenoise ONLY in production
    *(
        ["whitenoise.middleware.WhiteNoiseMiddleware"]
        if not DEBUG else []
    ),

    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 1024

ROOT_URLCONF = "config.urls"

# ==============================
# TEMPLATES
# ==============================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ==============================
# DATABASE
# ==============================
DATABASE_URL = env("DATABASE_URL", default=None)

if DATABASE_URL:
    import dj_database_url
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ==============================
# AUTH SECURITY
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Edmonton"
USE_TZ = True
USE_I18N = True

# ==============================
# STATIC + MEDIA
# ==============================

# FIXED STATIC URL
STATIC_URL = "/static/"

# Production uses Whitenoise manifest
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
    if not DEBUG else
    "django.contrib.staticfiles.storage.StaticFilesStorage"
)

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Artifact roots
DZI_ROOT = MEDIA_ROOT / "dzi"
THUMBNAIL_ROOT = MEDIA_ROOT / "thumbnails"
GROSS_ROOT = MEDIA_ROOT / "gross"
MODEL3D_ROOT = MEDIA_ROOT / "3d_models"

GROSS_URL = "gross/"
MODEL3D_URL = "3d_models/"

# ==============================
# SLIDE STORAGE ROOT (PROD/DEV SAFE)
# ==============================
SVS_SLIDE_ROOT = env(
    "SVS_SLIDE_ROOT",
    default=str(BASE_DIR / "svs_slides")   # dev fallback
)

# ==============================
# API / AUTH / CORS
# ==============================
if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    CSRF_TRUSTED_ORIGINS = []
else:
    CORS_ALLOWED_ORIGINS = [
        o.strip()
        for o in env(
            "CORS_ALLOWED_ORIGINS",
            default="https://giportal.ca"
        ).split(",")
        if o.strip()
    ]
    CSRF_TRUSTED_ORIGINS = [
        o.strip()
        for o in env(
            "CSRF_TRUSTED_ORIGINS",
            default="https://giportal.ca"
        ).split(",")
        if o.strip()
    ]

CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# ==============================
# EMAIL
# ==============================
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@example.com")
EMAIL_HOST = env("EMAIL_HOST", default=None)
EMAIL_PORT = env.int("EMAIL_PORT", default=587) if EMAIL_HOST else None
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default=None)
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default=None)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)

ALLOWED_EMAIL_DOMAINS = [
    d.strip() for d in env("ALLOWED_EMAIL_DOMAINS", default="").split(",") if d.strip()
]

ACTIVATION_BASE_URL = env("ACTIVATION_BASE_URL", default="http://localhost:5173")

# ==============================
# SIMPLE JWT
# ==============================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# ==============================
# SECURITY
# ==============================
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# Only enforce HSTS / redirects in production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = False  # flip to True if you want preload later
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    X_FRAME_OPTIONS = "SAMEORIGIN"
else:
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"
    X_FRAME_OPTIONS = "SAMEORIGIN"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"