from django.forms import ModelForm
from .models import SupportMessage


class SupportMessageForm(ModelForm):
    class Meta:
        model = SupportMessage
        fields = ["content"]
