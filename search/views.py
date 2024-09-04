from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from answers.models import Answer
from questions.models import Question


def home_index(request):
    return render(request, "home/index.html")


def search_form_index(request):
    return render(request, "search/search_form.html")


def search_view(request):
    query = request.GET.get("q", "")
    question_results = []
    answer_results = []

    print(f"Search query: {query}")

    if query:

        question_results = Question.objects.filter(
            Q(title__icontains=query)
            | Q(details__icontains=query)
            | Q(expectations__icontains=query)
        )
        answer_results = Answer.objects.filter(Q(content__icontains=query))

        print(f"Questions found: {question_results.count()}")
        print(f"Answers found: {answer_results.count()}")

    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        html = render_to_string(
            "search/search_results.html",
            {"question_results": question_results, "answer_results": answer_results},
        )
        return JsonResponse({"html": html})
    else:
        return render(
            request,
            "search/search_form.html",
            {"question_results": question_results, "answer_results": answer_results},
        )


def question_detail_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, "search/question_detail.html", {"question": question})
