from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from questions.models import Question


def home_index(request):
    return render(request, "home/index.html")


def search_form_index(request):
    return render(request, "search/search_form.html")


def search_view(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        results = Question.objects.filter(
            Q(title__icontains=query) | Q(details__icontains=query)
        )

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("search/search_results.html", {"results": results})
        return JsonResponse({"html": html})
    else:
        return render(request, "search/search_form.html", {"results": results})
