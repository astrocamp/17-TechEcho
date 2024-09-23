from django.forms import ModelForm
from django.forms.widgets import Textarea

from answers.models import Answer


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ["content"]
        widgets = {
            "content": Textarea(
                attrs={"class": "textarea textarea-bordered bg-white text-black"}
            ),
        }
        labels = {
            "content": "回答",
        }
