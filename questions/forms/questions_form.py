from django.forms import ModelForm
from django.forms.widgets import Textarea, TextInput

from questions.models import Question


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["title", "details"]
        widgets = {
            "title": TextInput(attrs={"class": "input input-bordered"}),
            "details": Textarea(attrs={"class": "textarea textarea-bordered"}),
        }
        labels = {
            "title": "問題",
            "details": "問題描述",
        }
