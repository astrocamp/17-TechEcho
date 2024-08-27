from django.forms import ModelForm

from questions.models import Question


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["title", "details", "expectations"]
