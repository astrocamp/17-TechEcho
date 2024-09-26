def question_vote(request, question) -> str:
    # to avoid DoesNotExist exception if not found
    if not request.user.is_authenticated:
        return "neither"

    if not question.voted_by(request.user):
        return "neither"

    return question.votes_set.get(user=request.user).vote_status


# only three states of (upvote, downvote) allowed
# 1. (False,False)
# 2. (True,False)
# 3. (False,True)
# current_status, vote_status_change -> new_status, count_change
# upvoted         downvoted             downvoted   -2
# upvoted         upvoted               neither     -1
# neither         downvoted             downvoted   -1
# neither         upvoted               upvoted     1
# downvoted       downvoted             neither     1
# downvoted       upvoted               upvoted     2
# return (new_vote_status, vote_count_change)
def validate_votes_input(
    current_vote_status: str, vote_status_change: str
) -> tuple[str, int]:
    # we only allow vote_status_change to be upvoted or downvoted
    if vote_status_change not in ("upvoted", "downvoted"):
        return (current_vote_status, 0)

    if current_vote_status == vote_status_change:
        return ("neither", -1 if vote_status_change == "upvoted" else 1)

    if current_vote_status == "neither":
        return (vote_status_change, 1 if vote_status_change == "upvoted" else -1)

    return (vote_status_change, -2 if vote_status_change == "downvoted" else 2)
