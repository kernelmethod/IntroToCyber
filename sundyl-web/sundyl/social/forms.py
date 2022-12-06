from django.forms import ModelForm
from .models import UserProfile, UserUpload


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["description", "avatar"]


class UserUploadForm(ModelForm):
    class Meta:
        model = UserUpload
        fields = ["upload", "public"]
