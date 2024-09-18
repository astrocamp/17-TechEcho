import uuid

import markdown
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BlogForm
from .models import Blog


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
    blog_list = Blog.objects.filter(is_draft=False).order_by("-created_at")
    paginator = Paginator(blog_list, 5)  # Show 5 blogs per page.

    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)

    return render(request, "blogs/index.html", {"blogs": blogs})


@login_required
def user_drafts(request):
    drafts = Blog.objects.filter(author=request.user, is_draft=True).order_by(
        "-created_at"
    )
    return render(request, "blogs/user_drafts.html", {"drafts": drafts})


@login_required
def new(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user

            action = request.POST.get("action")

            if action == "preview":
                content_html = markdown.markdown(form.cleaned_data["content"])

                return render(
                    request,
                    "blogs/new.html",
                    {"form": form, "blog": blog, "content_html": content_html},
                )

            elif action == "publish":
                blog.is_draft = False
                blog.save()
                return redirect("blogs:index")

            blog.is_draft = True
            blog.save()
            return redirect("blogs:index")

        return render(request, "blogs/new.html", {"form": form})

    else:
        form = BlogForm()
    return render(request, "blogs/new.html", {"form": form})


def show(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    content_html = markdown.markdown(
        blog.content,
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            "markdown.extensions.toc",
            "markdown.extensions.sane_lists",
        ],
    )

    blog.views += 1
    blog.save(update_fields=["views"])

    author_display_name = blog.author.get_display_name()

    return render(
        request,
        "blogs/show.html",
        {
            "blog": blog,
            "content_html": content_html,
            "author_display_name": author_display_name,
        },
    )


@login_required
def edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if blog.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this blog post.")

    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            action = request.POST.get("action")

            if action == "preview":
                content_html = markdown.markdown(
                    form.cleaned_data["content"],
                    extensions=[
                        "markdown.extensions.extra",
                        "markdown.extensions.codehilite",
                        "markdown.extensions.toc",
                    ],
                )
                return render(
                    request,
                    "blogs/edit.html",
                    {"form": form, "blog": blog, "content_html": content_html},
                )

            elif action == "update":
                blog = form.save()
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
        return HttpResponseForbidden("You are not allowed to delete this blog post.")

    if request.method == "POST":
        blog.delete()
        return redirect("blogs:index")
    return render(request, "blogs/delete.html", {"blog": blog})
