def get_ordered_answers(question, order_type):
    if order_type == "id":
        return question.answer_set.select_related("user").order_by("-id"), "id"
    else:
        return (
            question.answer_set.select_related("user").order_by("-votes_count", "-id"),
            "votes_count",
        )
