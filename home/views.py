from django.db.models import Q
from django.shortcuts import render

from .models import Question


def index(request):
    return render(request, "home/index.html")


def search_view(request):
    query = request.GET.get("q")
    results = None
    if query:
        results = Question.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    return render(request, "home/search_results.html", {"results": results})
