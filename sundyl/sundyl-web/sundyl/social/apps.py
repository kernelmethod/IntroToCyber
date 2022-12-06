from django.apps import AppConfig
from django.db.models.signals import post_save


class SocialConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sundyl.social"

    def ready(self):
        from . import signals

        post_save.connect(signals.create_user_profile)
