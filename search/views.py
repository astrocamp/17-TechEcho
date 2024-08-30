from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from home.models import Question
from django.template.loader import render_to_string


def index(request):
    return render(request, "home/index.html")


def index(request):
    return render(request, "search/search_form.html")


def search_view(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        results = Question.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("search/search_results.html", {"results": results})
        return JsonResponse({"html": html})
    else:
        return render(request, "search/search_form.html", {"results": results})
