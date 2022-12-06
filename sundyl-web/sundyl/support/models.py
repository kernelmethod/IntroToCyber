from django.contrib.auth.models import User
from django.db import models


class SupportMessage(models.Model):

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
