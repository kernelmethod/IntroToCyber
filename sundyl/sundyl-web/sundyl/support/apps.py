from django.apps import AppConfig
from django.db.models.signals import post_save


class SupportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sundyl.support"

    def ready(self):
        from . import signals

        post_save.connect(signals.create_initial_support_message)
