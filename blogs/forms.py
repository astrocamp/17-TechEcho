from django import forms

from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            "title",
            "content",
            "labels",
            "is_draft",
            "image",
        ]
        labels = {
            "title": "標題",
            "content": "內容",
            "labels": "標籤",
            "is_draft": "儲存為草稿",
            "image": "封面圖片",
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
            "labels": forms.TextInput(
                attrs={
                    "required": True,
                    "class": "input-bordered w-full border-2 border-blue-500 rounded-lg bg-white p-1 tagify--custom-dropdown",
                    "x-data": "tags_input",
                    "placeholder": "至少要填一個標籤，例如：Javascript、Python、C++、Ruby 或 Java",
                }
            ),
            "is_draft": forms.CheckboxInput(
                attrs={
                    "class": "w-6 h-6 text-blue-500 rounded focus:outline-none",
                    "id": "id_is_draft",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "w-full p-2 rounded-md focus:outline-none",
                    "id": "id_image",
                    "accept": "image/jpeg, image/png, image/webp, image/gif",
                }
            ),
        }


def clean_image(self):
    image = self.cleaned_data.get("image")
    if image:
        allowed_formats = ["image/jpeg", "image/png", "image/webp", "image/gif"]

        # Correct way to access content_type
        if image.file.content_type not in allowed_formats:
            raise forms.ValidationError(
                "Unsupported file format. Please upload an image in JPG, PNG, WEBP, or GIF format."
            )
    return image
