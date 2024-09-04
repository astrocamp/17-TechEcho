from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from answers.models import Answer, Vote
from questions.models import Question


@login_required
def index(request, id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=id)
        answer = question.answer_set.create(
            content=request.POST["content"], user=request.user
        )
        messages.success(request, "新增成功")
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


@login_required
def vote(request, id, vote_type):
    answer = get_object_or_404(Answer, id=id)
    vote = Vote.objects.filter(user=request.user, answer=answer).first()
    if vote:
        if vote.vote_type == vote_type:
            if vote_type == "upvote":
                answer.votes_count -= 1
            else:
                answer.votes_count += 1
            vote.delete()
        else:
            if vote_type == "upvote":
                answer.votes_count += 2
            else:
                answer.votes_count -= 2
            vote.vote_type = vote_type
            vote.save()
    else:
        Vote.objects.create(user=request.user, answer=answer, vote_type=vote_type)
        if vote_type == "upvote":
            answer.votes_count += 1
        else:
            answer.votes_count -= 1
    answer.save()
    return JsonResponse(answer.votes_count, safe=False)
