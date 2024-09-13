from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content"]
        labels = {
            "title": "標題",
            "content": "內容",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full p-2 border-2 border-blue-500 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "id": "id_title",  # You can define an id for the field
                    "placeholder": "請輸入標題",  # Optional placeholder text
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "w-full p-2 border-2 border-blue-500 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "id": "id_content",  # You can define an id for the textarea
                    "placeholder": "請輸入內容",  # Optional placeholder text
                }
            ),
        }
