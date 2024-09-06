from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from answers.models import Answer
from questions.models import Question


def index(request, id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=id)
        answer = question.answer_set.create(content=request.POST["content"])
        messages.success(request, "新增成功")
        return redirect("questions:show", id=id)


def delete(request, id):
    if request.method == "POST":
        answer = get_object_or_404(Answer, pk=id)
        answer.delete()
        messages.success(request, "刪除成功")
        return redirect("questions:show", id=answer.question.id)


def upvote(request, id):
    if request.method == "POST":
        answer = get_object_or_404(Answer, pk=id)
        answer.votes_count += 1
        answer.save()
        return redirect("questions:show", id=answer.question.id)


def downvote(request, id):
    if request.method == "POST":
        answer = get_object_or_404(Answer, pk=id)
        answer.votes_count -= 1
        answer.save()
        return redirect("questions:show", id=answer.question.id)
