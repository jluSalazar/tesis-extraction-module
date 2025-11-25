# extraction/apps.py
from django.apps import AppConfig

from apps import extraction


class ExtractionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.extraction'
    verbose_name = "Extraction Module"