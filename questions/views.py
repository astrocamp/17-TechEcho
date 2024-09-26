from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from answers.forms import AnswerForm
from answers.utils.answers import parse_answers
from lib.utils.labels import parse_form_labels
from lib.utils.pagination import paginate

from .forms import QuestionForm
from .models import Question, Votes
from .utils.question_user_votes import question_vote, validate_votes_input
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

        if form.is_valid() and parse_form_labels(form):
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            form.save_m2m()

            messages.success(request, "成功提問")
            return redirect("questions:index")

        messages.error(request, "輸入資料錯誤，請再嘗試")
        return render(request, "questions/new.html", {"form": form})

    questions = (
        Question.objects.select_related("user")
        .prefetch_related("labels")
        .order_by("-id")
    )
    questions = paginate(request, questions)

    return render(request, "questions/index.html", {"questions": questions})


@require_GET
def new(request):
    if request.user.is_anonymous:
        messages.error(request, "只有登入過使用者才能發問喔")
        return redirect("users:login")

    form = QuestionForm()
    return render(request, "questions/new.html", {"form": form})


def show(request, id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "請登入後再嘗試")
            return redirect("users:login")

        question = get_object_or_404(Question, pk=id, user=request.user)
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid() and parse_form_labels(form):
            form.save()

            messages.success(request, "編輯成功")
            return redirect("questions:show", id=id)

        messages.error(request, "編輯失敗")
        return render(
            request, "questions/edit.html", {"form": form, "question": question}
        )

    if not Question.all_objects.filter(pk=id).exists():
        raise Http404("沒有這個問題")

    question = Question.all_objects.get(pk=id)
    question_deleted = question.is_soft_deleted()

    answers = parse_answers(request, question, request.GET.get("order"))
    answers = paginate(request, answers, items_count=6)
    return render(
        request,
        "questions/show.html",
        {
            "question": question,
            "question_deleted": question_deleted,
            "answers": answers,
            "vote": None if question_deleted else question_vote(request, question),
            "form": None if question_deleted else AnswerForm(),
            "followed": (
                None if question_deleted else question.followed_by(request.user)
            ),
        },
    )


@login_required
@require_GET
def edit(request, id):
    question = get_object_or_404(
        Question.objects.prefetch_related("labels"), pk=id, user=request.user
    )
    form = QuestionForm(instance=question)
    return render(
        request,
        "questions/edit.html",
        {"form": form, "question": question},
    )


@login_required
@require_POST
def delete(request, id):
    question = get_object_or_404(Question, pk=id, user=request.user)
    question.delete()
    return redirect("questions:index")


@login_required
@require_POST
def votes(request, id):
    question = get_object_or_404(Question, pk=id)

    if not question.voted_by(request.user):
        record = Votes.objects.create(question=question, user=request.user)
    else:
        record = question.votes_set.get(user=request.user)

    vote_change = request.POST.get("vote_change")
    vote_status, actual_change = validate_votes_input(record.vote_status, vote_change)

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
@require_POST
def follows(request, id):
    question = get_object_or_404(Question, pk=id)
    if question.user == request.user:
        messages.error(request, "發文者已自動追蹤自己的問題，不必額外追蹤")
        return redirect("questions:show", id=id)

    channel_layer = get_channel_layer()
    channel_name = cache.get(f"notifications_user_{request.user.id}")
    if question.followed_by(request.user):
        question.followers.remove(request.user)
        if channel_name:
            async_to_sync(channel_layer.send)(
                channel_name,
                {
                    "type": "leave_group",
                    "group_name": f"notifications_questions_{question.id}",
                },
            )

    else:
        question.followers.add(request.user)
        if channel_name:
            async_to_sync(channel_layer.send)(
                channel_name,
                {
                    "type": "join_group",
                    "group_name": f"notifications_questions_{question.id}",
                },
            )

    return render(
        request,
        "questions/partials/_follows.html",
        {"question": question, "followed": question.followed_by(request.user)},
    )


@login_required
@require_POST
def preview(request):
    form = QuestionForm(request.POST)
    if form.is_valid():
        preview_content = form.cleaned_data.get("details", None)
        return render(
            request,
            "questions/partials/_preview.html",
            {"preview_content": preview_content},
        )

    warning = "請依以下規定改正後再預覽：" + " / ".join(
        map(lambda x: " / ".join(x), form.errors.values())
    )
    return render(
        request,
        "questions/partials/_preview.html",
        {"warning": warning},
    )
