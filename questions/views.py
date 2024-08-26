from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from .forms import QuestionForm
from django.contrib import messages
# Create your views here.


def index(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            messages.success(request, "question posted")
            return redirect("questions:index")

        messages.error(request, "submission fail, retry")
        return render(request, "questions/new.html", {"form": form})
    questions = Question.objects.order_by("-id")
    return render(request, "questions/index.html", {"questions": questions})


def new(request):
    form = QuestionForm()
    return render(request, "questions/new.html", {"form": form})


def show(request, id):
    question = get_object_or_404(Question, pk=id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            messages.success(request, "question edited")
            return redirect("questions:show", id=id)
        messages.error(request, "edit fail, retry")
        return render(request, "question/edit.html", {"form": form, "question": question})

    return render(request, "questions/show.html", {"question": question})


def edit(request, id):
    question = get_object_or_404(Question, pk=id)
    form = QuestionForm(instance=question)
    return render(request, "question/edit.html", {"form": form, "question": question})
