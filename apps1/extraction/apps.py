# extraction/apps.py
from django.apps import AppConfig

class ExtractionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'extraction'
    verbose_name = "Extraction Module"

    def ready(self):
        # Importamos las señales u otros efectos secundarios
        import extraction.workspace.signals