import os
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from sundyl.social.models import UserProfile
from sundyl.settings import BASE_DOMAIN
from urllib.parse import urlparse
from .mixins import LoginRequiredMixin


class SignupView(View):
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        context = {"form": form}

        if not form.is_valid():
            return render(request, "signup.html", context)

        new_user = form.save()

        # Create new profile for user
        # profile = UserProfile(user=new_user)
        # profile.save()

        login(request, new_user)
        return HttpResponseRedirect(reverse("index"))


class LogoutView(LoginRequiredMixin, View):

    # NOTE: intentionally vulnerable to CSRF
    def get(self, request, *args, **kwargs):
        referer = request.headers.get("Referer")

        # Our heuristic for determining whether or not there was a successful
        # CSRF is to check whether there's a Referer header. If there is, we
        # check if it corresponds to a different domain
        if referer is not None:
            url = urlparse(referer)

            if url.netloc not in (BASE_DOMAIN, f"www.{BASE_DOMAIN}"):
                # CSRF successful! We should update the user's profile to indicate that.
                profile = UserProfile.objects.filter(user__id=request.user.id).get()
                profile.successful_csrf = True
                profile.save()

        logout(request)
        return HttpResponseRedirect(reverse("index"))
