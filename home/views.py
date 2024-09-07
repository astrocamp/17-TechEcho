import json

from django.db.models import Q
from django.shortcuts import render

from questions.models import Question


def index(request):
    return render(request, "home/index.html")


def search(request):
    query = request.GET.get("q", "")
    search_terms = []
    questions = Question.objects.none()

    if query:
        search_terms = query.split()

        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(title__icontains=term) | Q(details__icontains=term)

        questions = Question.objects.filter(q_objects).distinct()

    return render(
        request,
        "home/search.html",
        {
            "questions": questions,
            "query": query,
        },
    )
