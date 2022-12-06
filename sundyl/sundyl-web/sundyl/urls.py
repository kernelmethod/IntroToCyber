"""sundyl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from pathlib import Path
from sundyl import settings
from .views import wildcard_page

urlpatterns = [
    path("", include("sundyl.social.urls")),
    path("", include("sundyl.search.urls")),
    path("support/", include("sundyl.support.urls")),
    path("auth/", include("sundyl.login.urls")),
    path("admin/", admin.site.urls),
]

if settings.USE_LOCAL_STORAGE:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


secret_page = Path("/") / "run" / "secrets" / "SECRET_PAGE"

if secret_page.exists():
    with open(secret_page, "r") as f:
        secret_page_route = f.readline().rstrip()
else:
    secret_page_route = "secret"

urlpatterns += [path(secret_page_route, wildcard_page)]
