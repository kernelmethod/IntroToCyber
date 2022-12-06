from django.forms.renderers import TemplatesSetting


class DefaultFormRenderer(TemplatesSetting):
    form_template_name = "form_snippet.html"
