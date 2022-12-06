# Additional views for the webapp

from django import http
from pathlib import Path


def wildcard_page(request):
    """View that shows the page enumeration wildcard flag."""

    flag = Path("/") / "run" / "secrets" / "FLAG_WILDCARD_PAGE_ENUMERATION"

    if flag.exists():
        with open(flag, "r") as f:
            flag = f.read()
    else:
        flag = "flag{wildcard:000000000}"

    return http.HttpResponse(flag, status=200)
