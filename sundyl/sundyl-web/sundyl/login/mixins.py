# Custom mixins for login, permissions, etc.

from django.contrib.auth.mixins import LoginRequiredMixin as _LoginRequiredMixin
from django.urls import reverse_lazy


class LoginRequiredMixin(_LoginRequiredMixin):
    login_url = reverse_lazy("login")
    redirect_field_name = "next"
