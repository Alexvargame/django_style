from django.apps import AppConfig


class EducaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'education.education_apps.educa'

    def ready(self):
        import education.education_apps.educa.signals
