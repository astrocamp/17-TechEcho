from django import forms
from django.forms.widgets import Textarea, TextInput

from questions.models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "details", "labels"]
        widgets = {
            "title": TextInput(
                attrs={
                    "required": "true",
                    "class": "input input-bordered border-blue-2 rounded-lg bg-white w-full py-1 px-3",
                    "placeholder": "標題最多五十個字",
                }
            ),
            "labels": TextInput(
                attrs={
                    "required": "true",
                    "x-data": "tags_input",
                    "class": "input-bordered border-blue-2 rounded-lg bg-white w-full p-1 tagify--custom-dropdown",
                    "placeholder": "至少要填一個標籤，例如：Javascript、Python、C++、Ruby 或 Java",
                }
            ),
            "details": Textarea(
                attrs={
                    "required": "true",
                    "class": "textarea textarea-bordered textarea-xs border-blue-2 rounded-lg bg-white w-full py-1 px-3 text-[17px]",
                    "placeholder": "問題內容至少要二十個字。",
                }
            ),
        }
        labels = {"title": "問題", "labels": "標籤", "details": "問題內容"}
        error_messages = {
            "title": {
                "required": "請輸入問題標題",
                "max_length": "問題標題最多只能五十個字",
            },
            "labels": {"required": "請輸入至少一個標籤"},
            "details": {
                "required": "請輸入問題內容",
            },
        }
