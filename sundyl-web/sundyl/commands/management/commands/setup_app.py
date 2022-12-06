#!/usr/bin/env python3

import os
import random
from django.contrib.auth.models import User, Group
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from sundyl import settings
from sundyl.social.models import UserProfile, UserUpload
from secrets import token_urlsafe
from pathlib import Path

COMMAND_DIR = Path(__file__).resolve().parent
DEFAULT_PROFILE_IMAGE = COMMAND_DIR / "profile_default.png"


def setup_staff():
    """Set up the staff group and all staff members."""

    if not Group.objects.filter(name="staff").exists():
        Group.objects.create(name="staff")

    staff = Group.objects.get(name="staff")
    usernames = ("jodi_crockwell", "freddy_obrzut", "kirby_elledge")
    descriptions = (
        "Software reliability and security senior engineer @ Sundyl",
        "IT and customer support for Sundyl",
        "Marketing and outreach coordinator",
    )
    avatars = (
        "jodi.webp",
        "freddy.webp",
        "kirby.webp",
    )

    for (name, description, img) in zip(usernames, descriptions, avatars):
        if not User.objects.filter(username=name).exists():
            user = User(username=name)
            if name.startswith("freddy"):
                with open("/run/secrets/STAFF_PASSWORD", "r") as f:
                    password = f.readline().rstrip()
            else:
                password = token_urlsafe()
            user.set_password(password)
            user.save()

        user = User.objects.get(username=name)
        user.is_staff = True
        user.save()
        staff.user_set.add(user)

        # Set up profile
        profile = UserProfile.objects.filter(user=user).get()
        profile.description = description
        with open(COMMAND_DIR / img, "rb") as f:
            img = f.read()
        path = default_storage.save(profile.avatar_path(), ContentFile(img))
        profile.avatar.name = profile.avatar_path()
        profile.save()

    # Create a non-staff user whose bio contains the user enumeration flag
    if not User.objects.filter(username="otis_eugene_ray").exists():
        otis = User(username="otis_eugene_ray", id=133)
        otis.set_password(token_urlsafe(16))
        otis.save()

    with open("/run/secrets/FLAG_USERS", "r") as f:
        flag = f.read()

    otis = User.objects.filter(username="otis_eugene_ray").get()
    profile = UserProfile.objects.filter(user=otis).get()
    profile.description = flag
    profile.save()


def add_default_uploads():
    """Add some default file uploads for the users that currently exist."""

    kirby = User.objects.get(username="kirby_elledge")
    profile = UserProfile.objects.filter(user=kirby).get()

    with open("/run/secrets/FLAG_SQLI", "rb") as f:
        flag = f.read().rstrip()

    flag_file_name = "sup3r-s3cret-sqli-flag.txt"
    path = profile.construct_media_path(flag_file_name)

    if not UserUpload.objects.filter(user=kirby, upload=path).exists():
        upload = UserUpload(user=kirby, public=False, upload=ContentFile(flag, name=flag_file_name))
        upload.save()

    with open(COMMAND_DIR / "logo.png", "rb") as f:
        img = f.read()

    for filename in ("logo.png", "sundyl.png"):
        path = profile.construct_media_path(filename)
        if not UserUpload.objects.filter(user=kirby, upload=path).exists():
            upload = UserUpload(user=kirby, public=True, upload=ContentFile(img))
            upload.upload.name = path
            upload.save()

    # Add default profile image
    with open(DEFAULT_PROFILE_IMAGE, "rb") as f:
        data = f.read()
    path = default_storage.save(settings.DEFAULT_PROFILE_IMAGE, ContentFile(data))

    # Add default admin script
    DEFAULT_SCRIPT = b"""\
#!/bin/bash

echo "The current time is: $(date)"
"""
    default_storage.save("admin-scripts/example.sh", ContentFile(DEFAULT_SCRIPT))


class Command(BaseCommand):
    help = "Create base users, groups, and more for the webapp"

    def add_arguments(self, parser):
        ...

    def handle(self, *args, **options):
        setup_staff()
        add_default_uploads()
