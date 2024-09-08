import json
from http.client import HTTPResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render

from answers.forms import AnswerForm
from answers.models import Answer
from lib.utils.pagination import paginate

from .forms import QuestionForm
from .models import Question, QuestionUserVotes
from .utils.labels import parse_labels
from .utils.question_user_votes import (
    upvoted_or_downvoted_or_neither,
    validate_votes_input,
)
from .utils.sort import order_is_valid


def index(request):
    # partial rendering only
    if request.htmx and request.htmx.request.method == "GET":
        order = request.GET.get("order")
        questions = Question.objects.order_by(order if order_is_valid(order) else "-id")
        questions = paginate(request, questions)
        return render(
            request, "questions/partials/_questions_list.html", {"questions": questions}
        )

    elif request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "請登入後再嘗試")
            return redirect("users:login")

        form = QuestionForm(request.POST)
        labels = parse_labels(request.POST)

        if labels and form.is_valid():
            # commit=False is not applicable here because instance.labels.set(labels) requires a pk
            # and since our pk is defined by the ORM not by us, it will only exist once we save it to the DB
            instance = form.save()
            instance.labels.set(labels)
            instance.user = request.user
            instance.save()

            messages.success(request, "成功提問")
            return redirect("questions:index")

        messages.error(request, "輸入資料錯誤，請再嘗試")
        return render(request, "questions/new.html", {"form": form})

    questions = Question.objects.prefetch_related("labels").order_by("-id")
    questions = paginate(request, questions, items_count=5)
    return render(request, "questions/index.html", {"questions": questions})


def new(request):
    form = QuestionForm()
    return render(request, "questions/new.html", {"form": form})


def show(request, id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "請登入後再嘗試")
            return redirect("users:login")

        question = get_object_or_404(Question, pk=id, user=request.user)
        form = QuestionForm(request.POST, instance=question)
        labels = parse_labels(request.POST)

        if labels and form.is_valid():
            instance = form.save(commit=False)
            instance.labels.set(labels)
            instance.save()
            form.save_m2m()

            messages.success(request, "編輯成功")
            return redirect("questions:show", id=id)

        messages.error(request, "編輯失敗")
        return render(
            request, "questions/edit.html", {"form": form, "question": question}
        )

    question = get_object_or_404(Question, pk=id)
    vote = upvoted_or_downvoted_or_neither(request, question)

    answers = question.answer_set.order_by("-votes_count", "-id")
    answers = paginate(request, answers, items_count=10)
    form = AnswerForm()
    return render(
        request,
        "questions/show.html",
        {
            "question": question,
            "answers": answers,
            "vote": vote,
            "form": form,
            "followed": question.followed_by(request.user),
        },
    )


@login_required
def edit(request, id):
    question = get_object_or_404(Question, pk=id, user=request.user)
    form = QuestionForm(instance=question)
    return render(
        request,
        "questions/edit.html",
        {"form": form, "question": question, "labels": question.labels.all()},
    )


@login_required
def delete(request, id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=id, user=request.user)
        question.delete()
        return redirect("questions:index")


@login_required
def votes(request, id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=id)

        if not question.has_voted(request.user):
            record = QuestionUserVotes.objects.create(
                question=question, user=request.user
            )
        else:
            record = question.questionuservotes_set.get(user=request.user)

        vote_change = request.POST.get("vote_change")
        vote_status, actual_change = validate_votes_input(
            record.vote_status, vote_change
        )

        record.vote_status = vote_status
        record.save()

        question.votes_count += actual_change
        question.save()

        return render(
            request,
            "questions/partials/_votes.html",
            {
                "question": question,
                "vote": record.vote_status,
            },
        )


@login_required
def follows(request, id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=id)
        if question.user == request.user:
            messages.error(request, "發文者已自動追蹤自己的問題，不必額外追蹤")
            return redirect("questions:show", id=id)

        if question.followed_by(request.user):
            question.followers.remove(request.user)
        else:
            question.followers.add(request.user)

        return render(
            request,
            "questions/partials/_follows.html",
            {"question": question, "followed": question.followed_by(request.user)},
        )
