from django import template

register = template.Library()


@register.filter(name="check_vote")
def check_vote(vote, condition):
    return "solid" if vote == condition else "regular"
