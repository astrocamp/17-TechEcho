from django import forms

from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            "title",
            "content",
            "category",
            "is_draft",
        ]
        labels = {
            "title": "標題",
            "content": "內容",
            "category": "類別",
            "is_draft": "儲存為草稿",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full p-2 border-2 border-blue-500 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "id": "id_title",
                    "placeholder": "請輸入標題",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "w-full p-2 border-2 border-blue-500 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "id": "id_content",
                    "placeholder": "請輸入內容",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "w-full p-2 border-2 border-blue-500 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "id": "id_category",
                }
            ),
            "is_draft": forms.CheckboxInput(
                attrs={
                    "class": "w-6 h-6 text-blue-500 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "id": "id_is_draft",
                }
            ),
        }
