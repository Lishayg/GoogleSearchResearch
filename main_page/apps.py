from django.apps import AppConfig


class CodingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_page'
    verbose_name = 'Collected Data'

    def ready(self):
        # Import and connect the signal here
        from . import signals
