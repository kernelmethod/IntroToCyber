from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SupportMessage
from .utils import get_support_user
from sundyl import settings


@receiver(post_save, sender=User)
def create_initial_support_message(sender, instance, created, **kwargs):
    """Whenever a new user is created, send them an initial support message."""
    if not created or not isinstance(instance, User):
        return

    if SupportMessage.objects.filter(to_user__id=instance.id).count() > 0:
        return

    initial_message = (
        f"Welcome to {settings.BASE_DOMAIN}!\n\n"
        "Are you having trouble with our website? Please send me a link to the page "
        f"you're having trouble with on our trusty {settings.BASE_DOMAIN} domain "
        "and I will check it out!"
    )

    try:
        msg = SupportMessage(
            from_user=get_support_user(),
            to_user=instance,
            content=initial_message,
        )
        msg.save()
    except User.DoesNotExist:
        print("Skipping initial support message; support user does not exist")
