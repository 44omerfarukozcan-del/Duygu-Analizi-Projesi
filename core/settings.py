from pathlib import Path
import os

# Temel dizin yolu
BASE_DIR = Path(__file__).resolve().parent.parent

# GÜVENLİK: Canlı ortamda bu anahtarı .env dosyası ile gizleyeceğiz
SECRET_KEY = 'django-insecure-kendi-gizli-anahtarini-buraya-yaz'

# GÜVENLİK: Sunucuya çıktığımızda DEBUG = False olmak ZORUNDA
DEBUG = True

# ALAN ADI İZNİ: Sisteme erişebilecek yasal adresler
ALLOWED_HOSTS = ['kurumsesi.com', 'www.kurumsesi.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Kendi yazdığın uygulamalar:
    # 'core', 
    # 'analyzer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# DİKKAT: Kendi ana proje klasörünün adını yaz (Örn: 'kurumsesi.urls')
ROOT_URLCONF = 'projenin_ana_klasoru.urls' 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # HTML dosyalarının aranacağı kök klasör
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# DİKKAT: Kendi ana proje klasörünün adını yaz
WSGI_APPLICATION = 'projenin_ana_klasoru.wsgi.application' 


# --- VERİTABANI AYARLARI ---
# VSC üzerinde çalışırken SQLite aktif kalacak.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Sunucuya bağlandığımızda üstteki SQLite kodunu yoruma alıp bunu açacağız:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'kurumsesi_db',
#         'USER': 'kurumsesi_user',
#         'PASSWORD': 'sunucuda_belirleyecegimiz_sifre',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# --- BÖLGESEL AYARLAR ---
LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True


# --- STATİK VE MEDYA DOSYALARI ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"] 
STATIC_ROOT = BASE_DIR / 'staticfiles'   

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_HOST_USER = 'noreply.sistem.merkezi@gmail.com'
EMAIL_HOST_PASSWORD = 'itzuhjxwqjkqnkko'
DEFAULT_FROM_EMAIL = 'Kurum Sesi Bildirim <noreply.sistem.merkezi@gmail.com>'

# --- LOGLAMA (HATA TAKİBİ) ---
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}


# --- GÜVENLİK VE HTTPS AYARLARI (CANLI ORTAMDA AÇILACAK) ---
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True


# --- ASENKRON GÖREV YÖNETİMİ (YAPAY ZEKA İÇİN - CELERY & REDIS) ---
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'