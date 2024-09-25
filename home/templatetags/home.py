import markdown
import markdown2
from django import template
from django.template.defaultfilters import date as date_filter
from django.template.defaultfilters import stringfilter
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.timezone import localtime

register = template.Library()


@register.filter(name="standard_date")
def standard_date(value):
    value = localtime(value)
    return date_filter(value, "Y/m/d H:i")


@register.filter(name="strip_markdown_safe")
@stringfilter
def strip_markdown_safe(value):
    value = strip_tags(value)
    value = markdown2.markdown(
        value,
        extras=[
            "fenced-code-blocks",
            "tables",
            "footnotes",
            "toc",
            "strike",
            "task_list",
            "wiki-tables",
            "header-ids",
        ],
    )
    return mark_safe(value)
