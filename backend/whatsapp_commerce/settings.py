import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load environment variables from .env file (works locally)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# 🔐 SECURITY SETTINGS
# -----------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = ['*']

# ALLOWED_HOSTS = [
#     "whatsapp-ecommerce-evls.onrender.com",  # your Render domain
#     "localhost",
#     "127.0.0.1",
#     os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
# ]  # On Render, use ["your-service-name.onrender.com"]

# -----------------------------
# 📞 TWILIO WHATSAPP CONFIG
# -----------------------------
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# -----------------------------
# 🧩 INSTALLED APPS
# -----------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "corsheaders",
    "django_celery_beat",

    # Local apps
    "users",
    "products",
    "orders",
    "promotions",
    "whatsapp",
    "mpesa",
]

AUTH_USER_MODEL = "users.User"

# -----------------------------
# ⚙️ MIDDLEWARE
# -----------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ✅ For static file serving on Render
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "whatsapp_commerce.urls"

# -----------------------------
# 🧱 TEMPLATES
# -----------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "../frontend/build"],  # ✅ Serve React build
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

WSGI_APPLICATION = "whatsapp_commerce.wsgi.application"

# -----------------------------
# 🗄 DATABASE
# -----------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

# -----------------------------
# 🌍 REST FRAMEWORK
# -----------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

# -----------------------------
# 🌐 CORS
# -----------------------------
CORS_ALLOW_ALL_ORIGINS = True  # Allow all during testing
# Later, restrict with:
# CORS_ALLOWED_ORIGINS = ["https://your-frontend.onrender.com"]

# -----------------------------
# 🖼 STATIC & MEDIA FILES
# -----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ✅ Serve React frontend
STATICFILES_DIRS = [
    BASE_DIR / "../frontend/build/static",
]

# -----------------------------
# 🕒 CELERY CONFIG
# -----------------------------
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_BEAT_SCHEDULE = {
    "send-daily-product-summary": {
        "task": "promotions.tasks.send_daily_product_summary",
        "schedule": 86400,
    },
}

# -----------------------------
# 🔑 API KEYS
# -----------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")

# -----------------------------
# ⏰ TIME & LANGUAGE
# -----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
