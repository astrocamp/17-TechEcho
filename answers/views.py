from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from answers.models import Answer, Vote
from questions.models import Question


@login_required
@require_POST
def index(request, id):
    question = get_object_or_404(Question, pk=id)
    question.answer_set.create(content=request.POST["content"], user=request.user)
    messages.success(request, "新增成功")
    return redirect("questions:show", id=id)


@login_required
@require_POST
def delete(request, id):
    answer = get_object_or_404(Answer, pk=id, user=request.user)
    answer.delete()
    messages.success(request, "刪除成功")
    return redirect("questions:show", id=answer.question.id)


@login_required
@require_POST
def edit(request, id):
    answer = get_object_or_404(Answer, pk=id, user=request.user)
    answer.content = request.POST["content"]
    answer.save()
    return render(request, "answers/_answer_content.html", {"answer": answer})


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
            voted = "neither"
        else:
            if vote_type == "upvote":
                answer.votes_count += 2
                voted = "upvote"
            else:
                answer.votes_count -= 2
                voted = "downvote"
            vote.vote_type = vote_type
            vote.save()
    else:
        Vote.objects.create(user=request.user, answer=answer, vote_type=vote_type)
        if vote_type == "upvote":
            answer.votes_count += 1
            voted = "upvote"
        else:
            answer.votes_count -= 1
            voted = "downvote"
    answer.save()

    return render(
        request, "answers/partials/_votes.html", {"answer": answer, "voted": voted}
    )
