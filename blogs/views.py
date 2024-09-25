import base64
import os
import tempfile
import uuid

import markdown2
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from storages.backends.s3boto3 import S3Boto3Storage

from lib.utils.labels import parse_form_labels

from .forms import BlogForm
from .models import Blog

User = get_user_model()

MARKDOWN2_EXTRAS = [
    "fenced-code-blocks",
    "tables",
    "footnotes",
    "toc",
    "strike",
    "task_list",
    "wiki-tables",
    "header-ids",
    # Add more extras if needed
]


@login_required
def image_upload(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]

        if image.size > 2 * 1024 * 1024:
            return JsonResponse({"error": "File too large (max 2MB)."}, status=400)

        if not image.content_type.startswith("image/"):
            return JsonResponse({"error": "Invalid file type."}, status=400)

        extension = image.name.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{extension}"

        save_path = default_storage.save(
            "uploads/" + unique_filename, ContentFile(image.read())
        )
        image_url = settings.MEDIA_URL + save_path

        return JsonResponse({"url": image_url})

    return JsonResponse({"error": "Invalid request"}, status=400)


def index(request):
    blog_list = (
        Blog.objects.filter(is_draft=False)
        .prefetch_related("labels")
        .order_by("-created_at")
    )
    paginator = Paginator(blog_list, 5)

    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)

    return render(request, "blogs/index.html", {"blogs": blogs})


@login_required
def like(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    user = request.user

    if user in blog.likes.all():
        blog.likes.remove(user)
        liked = False
    else:
        blog.likes.add(user)
        liked = True

    likes_count = blog.likes.count()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"liked": liked, "likes_count": likes_count})
    else:
        return HttpResponseRedirect(reverse("blogs:show", args=[blog_id]))


@login_required
def user_drafts(request):
    drafts = Blog.objects.filter(author=request.user, is_draft=True).order_by(
        "-created_at"
    )
    return render(request, "blogs/user_drafts.html", {"drafts": drafts})


@login_required
def new(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid() and parse_form_labels(form):
            blog = form.save(commit=False)
            blog.author = request.user

            action = request.POST.get("action")

            if action == "preview":
                content_html = markdown2.markdown(
                    form.cleaned_data["content"],
                    extras=MARKDOWN2_EXTRAS,
                )

                return render(
                    request,
                    "blogs/new.html",
                    {
                        "form": form,
                        "blog": blog,
                        "content_html": content_html,
                    },
                )

            elif action == "publish":
                blog.is_draft = False
                blog.save()
                form.save_m2m()
                return redirect("blogs:index")

            # Handle 'save_draft' action
            blog.is_draft = True
            blog.save()
            form.save_m2m()
            return redirect("blogs:index")

        return render(request, "blogs/new.html", {"form": form})

    else:
        form = BlogForm()
    return render(request, "blogs/new.html", {"form": form})


def show(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    content_html = markdown2.markdown(
        blog.content,
        extras=MARKDOWN2_EXTRAS,
    )

    blog.views += 1
    blog.save(update_fields=["views"])

    author_display_name = blog.author.get_display_name()

    # Check if the user is authenticated and has liked the blog
    user_liked = False
    if request.user.is_authenticated:
        user_liked = request.user in blog.likes.all()

    return render(
        request,
        "blogs/show.html",
        {
            "blog": blog,
            "content_html": content_html,
            "author_display_name": author_display_name,
            "user_liked": user_liked,
        },
    )


@login_required
def edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if blog.author != request.user:
        return HttpResponseForbidden("你不被允許編輯此部落格文章。")

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid() and parse_form_labels(form):
            action = request.POST.get("action")

            if action == "preview":
                content_html = markdown2.markdown(
                    form.cleaned_data["content"],
                    extras=MARKDOWN2_EXTRAS,
                )

                preview_image = form.cleaned_data.get("image", "???????????")

                return render(
                    request,
                    "blogs/edit.html",
                    {
                        "form": form,
                        "blog": blog,
                        "content_html": content_html,
                        "preview_image": preview_image,
                    },
                )

            elif action == "update":
                blog = form.save()
                return redirect("blogs:show", pk=blog.pk)

            elif action == "publish":
                blog = form.save()
                blog.publish()
                return redirect("blogs:show", pk=blog.pk)

            elif action == "save_draft":
                blog = form.save(commit=False)
                blog.is_draft = True
                blog.save()
                return redirect("blogs:user_drafts")

    else:
        form = BlogForm(instance=blog)

    return render(request, "blogs/edit.html", {"form": form, "blog": blog})


@login_required
def delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if blog.author != request.user:
        return HttpResponseForbidden("你不被允許刪除此部落格文章。")

    if request.method == "POST":
        blog.delete()
        return redirect("blogs:index")
    return render(request, "blogs/delete.html", {"blog": blog})
