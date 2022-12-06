from django.contrib.auth.models import User
from django.test import TestCase
from .models import UserProfile
from sundyl import settings


class UserProfileTestCases(TestCase):
    """Tests to ensure that user profiles and related basic functionality work correctly."""

    def setUp(self):
        # Create some initial users
        User(username="alice").save()
        User(username="bob").save()

    def test_user_profile_is_automatically_set_up(self):
        """User profiles should automatically be set up when a user is created."""

        self.assertTrue(UserProfile.objects.filter(user__username="alice").exists())
        self.assertTrue(UserProfile.objects.filter(user__username="bob").exists())

        # Check defaults for newly-initialized profiles
        profile = UserProfile.objects.filter(user__username="alice").get()
        self.assertEqual(profile.description, "")
        self.assertEqual(profile.avatar.name, settings.DEFAULT_PROFILE_IMAGE)
        self.assertFalse(profile.successful_csrf)
        self.assertFalse(profile.successful_xss)
        self.assertEqual(profile.followers.count(), 0)
