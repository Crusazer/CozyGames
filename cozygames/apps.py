from django.apps import AppConfig


class CozygamesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cozygames'

    def ready(self):
        import cozygames.schedule_tasks
