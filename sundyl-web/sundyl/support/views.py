import re

import requests
import typing as _t
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from sundyl.login.mixins import LoginRequiredMixin
from .forms import SupportMessageForm
from .models import SupportMessage
from .utils import get_support_user
from urllib.parse import urlparse
from multiprocessing import Process


URL_REGEX = r"(https?://)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
URL_REGEX = re.compile(URL_REGEX)


class SupportView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = SupportMessageForm()
        context = {
            "form": form,
            "support": get_support_user(),
            "messages": self._messages(request),
        }
        return render(request, "support.html", context)

    def post(self, request, *args, **kwargs):
        form = SupportMessageForm(request.POST)

        if not form.is_valid():
            return HttpResponse("Invalid message", status=422)

        msg = SupportMessage(
            from_user=request.user,
            to_user=get_support_user(),
            content=form.cleaned_data["content"],
        )
        msg.save()
        reply = SupportMessage(
            from_user=get_support_user(),
            to_user=request.user,
            content=self._handle_message(request, msg),
        )
        reply.save()

        context = {
            "form": SupportMessageForm(),
            "support": get_support_user(),
            "messages": self._messages(request),
        }

        return render(request, "support.html", context)

    def _messages(self, request) -> _t.Iterable[User]:
        return SupportMessage.objects.filter(
            Q(from_user__id=request.user.id) | Q(to_user__id=request.user.id)
        )

    def _handle_message(self, request, msg: SupportMessage) -> str:
        # Extract URL from input message, if there is one

        if (match := URL_REGEX.match(msg.content)) is None:
            return (
                "I'm not sure I understood your question. Can you try sending me "
                "a link to the page you're having trouble with?"
            )

        url = match.group(0)
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "http://" + url

        url_components = urlparse(url)
        if url_components.netloc not in ("www.sundyl.lab", "sundyl.lab"):
            return "Sorry, I only visit links from our very trustworth www.sundyl.lab domain"

        support_server = "http://support.sundyl.lab:5000"
        resp = requests.get(f"{support_server}/visit", json={"url": url})
        return "Okay, I will take a look at your page!"


class MessageView(View):
    def get(self, request, *args, **kwargs):
        # Render the message corresponding to the request

        if (message_id := kwargs.get("message_id")) is None:
            return HttpResponse("No message id was provided", status=400)

        try:
            msg = SupportMessage.objects.filter(id=message_id).get()
        except SupportMessage.DoesNotExist:
            return HttpResponse("No message with the given ID was found", status=404)

        return render(request, "viewmessage.html", {"msg": msg})
