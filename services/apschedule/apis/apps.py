from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apis"

    def ready(self):
        import apis.schedulers

        apis.schedulers.start_scheduler()
