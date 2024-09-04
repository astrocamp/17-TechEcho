from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="question_labels")
def question_labels(question):
    return question.labels.all()
