from django import template


register = template.Library()


@register.inclusion_tag("profile_short.html")
def profile_short(profile):
    return {"profile": profile}
