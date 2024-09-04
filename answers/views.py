from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from answers.models import Answer
from questions.models import Question


@login_required
def index(request, id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=id)
        answer = question.answer_set.create(
            content=request.POST["content"], user=request.user
        )
        return redirect("questions:show", id=id)
    question = get_object_or_404(Question, pk=id)
    answers = question.answer_set.all()
    return render(
        request,
        "answers/index.html",
        {"question": question, "answers": answers, "user": request.user},
    )


@csrf_exempt
@login_required
def delete(request, id):
    if request.method == "POST":
        answer = get_object_or_404(Answer, pk=id)
        if answer.user == request.user:
            answer.delete()
        return redirect("questions:show", id=answer.question.id)


@login_required
def update(request, id):
    if request.method == "POST":
        answer = get_object_or_404(Answer, pk=id)
        if answer.user == request.user:
            answer.content = request.POST["content"]
            answer.save()
            return render(request, "answers/_answer_content.html", {"answer": answer})
    return JsonResponse({"success": False}, status=400)
