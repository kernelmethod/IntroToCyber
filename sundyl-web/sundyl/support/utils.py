# Common utilities for the support app

from django.contrib.auth.models import User


def get_support_user() -> User:
    return User.objects.filter(username="freddy_obrzut").get()
