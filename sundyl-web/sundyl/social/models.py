from django.core.files import File
from django.db import models
from django.contrib.auth.models import User
from django.db.models.constraints import UniqueConstraint
from sundyl import settings


def avatar_path(instance, filename: str) -> str:
    avatar = f"avatars/{instance.user.username}/avatar"
    return avatar


def user_directory_path(instance, filename: str) -> str:
    return f"uploads/{instance.user.username}/{filename}"


class UserProfile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="profile"
    )
    description = models.TextField()
    avatar = models.ImageField(upload_to=avatar_path, default=settings.DEFAULT_PROFILE_IMAGE)
    successful_csrf = models.BooleanField(default=False)
    successful_xss = models.BooleanField(default=False)

    def avatar_path(self) -> str:
        return avatar_path(self, "avatar")

    def construct_media_path(self, filename: str) -> str:
        return user_directory_path(self, filename)

    @property
    def num_followers(self) -> int:
        return self.followers.count()


class UserFollowing(models.Model):

    source_user = models.ForeignKey(UserProfile, related_name="following", on_delete=models.CASCADE)
    dest_user = models.ForeignKey(UserProfile, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["source_user", "dest_user"], name="unique_follower")
        ]


class UserUpload(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload = models.FileField(upload_to=user_directory_path)

    # Whether or not the upload is publicly listed. This only affects the listing; the upload
    # can still be shared with other users.
    public = models.BooleanField(default=False)
