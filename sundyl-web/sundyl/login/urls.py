from django.contrib.auth import views as auth_views
from django.urls import path
from .views import SignupView, LogoutView

urlpatterns = [
    path("login", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("signup", SignupView.as_view(), name="signup"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("change_password", auth_views.PasswordChangeView.as_view(), name="change_password"),
]
