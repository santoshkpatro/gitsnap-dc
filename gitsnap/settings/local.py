import os
from dotenv import load_dotenv

from gitsnap.settings.base import *
load_dotenv()

# Database Config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PG_NAME', 'gitsnap'),
        'USER': os.environ.get('PG_NAME', 'gitsnap'),
        'PASSWORD': os.environ.get('PG_PASSWORD', 'gitsnap'),
        'HOST': os.environ.get('PG_HOST', 'localhost'),
        'PORT': os.environ.get('PG_PORT', '5432'),
    }
}

# MEDIA Settings
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'