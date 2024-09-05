from django import template

register = template.Library()


@register.filter(name="question_labels")
def question_labels(question):
    return question.labels.all()
