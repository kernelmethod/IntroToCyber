from django.shortcuts import render
from django.views.generic import View
from sundyl.login.mixins import LoginRequiredMixin
from sundyl.search.forms import SearchForm
from sundyl.social.models import UserUpload


class SearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET)

        if not form.is_valid():
            return render(request, "search.html", {"form": SearchForm(), "results": None})

        # NOTE: the following query is intentionally vulnerable to SQL injection
        table = UserUpload.objects.model._meta.db_table
        query = (
            f"SELECT * FROM {table} "
            f"WHERE upload ~ '{form.cleaned_data['search_term']}' AND public"
        )

        results = list(UserUpload.objects.raw(query))
        return render(request, "search.html", {"form": form, "results": results})
