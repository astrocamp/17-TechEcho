import json

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from answers.forms import AnswerForm

from .forms import QuestionForm
from .models import Question


def index(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        labels = request.POST.get("labels")

        # we require at least one label
        if labels and form.is_valid():
            instance = form.save()
            labels = [label["value"] for label in json.loads(labels)]

            instance.labels.set(labels)
            instance.save()
            messages.success(request, "成功提問")
            return redirect("questions:index")

        messages.error(request, "輸入資料錯誤，請再嘗試")
        return render(request, "questions/new.html", {"form": form})

    order_by = request.GET.get("order_by")
    questions = Question.objects.order_by(order_by or "-id")
    return render(request, "questions/index.html", {"questions": questions})


def new(request):
    form = QuestionForm()
    return render(request, "questions/new.html", {"form": form})


def show(request, id):
    question = get_object_or_404(Question, pk=id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        labels = request.POST.get("labels")
        # we require at least one label
        if labels and form.is_valid():
            instance = form.save(commit=False)
            labels = [label["value"] for label in json.loads(labels)]
            instance.labels.set(labels)
            instance.save()
            form.save_m2m()

            messages.success(request, "編輯成功")
            return redirect("questions:show", id=id)

        messages.error(request, "編輯失敗")
        return render(
            request, "questions/edit.html", {"form": form, "question": question}
        )
    answers = question.answer_set.order_by("-id")
    form = AnswerForm()
    return render(
        request,
        "questions/show.html",
        {
            "question": question,
            "answers": answers,
            "form": form,
            "labels": question.labels.all(),
        },
    )


def edit(request, id):
    question = get_object_or_404(Question, pk=id)
    form = QuestionForm(instance=question)
    return render(
        request,
        "questions/edit.html",
        {"form": form, "question": question, "labels": question.labels.all()},
    )


def delete(request, id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=id)
        question.delete()
        return redirect("questions:index")


def votes(request, id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=id)
        votes_change = request.POST.get("votes_change")
        # only predefined change in value is allowed
        if votes_change in ("1", "-1"):
            question.votes_count += int(votes_change)
            question.save()

        return redirect("questions:show", id=id)
