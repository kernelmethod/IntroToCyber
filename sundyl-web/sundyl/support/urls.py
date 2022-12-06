from django.urls import path
from .views import SupportView, MessageView

urlpatterns = [
    path("", SupportView.as_view(), name="support"),
    path("viewmessage/<int:message_id>", MessageView.as_view(), name="view_message"),
]
