from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Whenever a new user is created, give them a profile."""
    if not created or not isinstance(instance, User):
        return

    profile = UserProfile(user=instance)
    profile.save()
