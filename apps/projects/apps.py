from django.apps import AppConfig

class ProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # ERROR ACTUAL: Probablemente dice 'projects' o 'old.projects'
    # CORRECCIÓN:
    name = 'apps.projects'
    verbose_name = "Projects Context"