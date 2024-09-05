from django import forms

from teachers.models import TeacherInfo


class TeacherInfoForm(forms.ModelForm):
    class Meta:
        model = TeacherInfo
        fields = ["user", "expertise", "introduce"]
        widgets = {
            "introduce": forms.Textarea(
                attrs={
                    "rows": 5,
                    "cols": 40,
                    "placeholder": "自我介紹",
                    "class": "custom-textarea",
                }
            ),
            "expertise": forms.TextInput(
                attrs={
                    "placeholder": "Ex:JavaScript..Python..",
                    "class": "custom-input",
                }
            ),
        }
        labels = {
            "user": "使用者",
            "expertise": "專業能力",
            "introduce": "自我介紹",
        }
